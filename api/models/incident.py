from api.utilitiez.auth_token import get_current_identity, is_admin_user
from database.db import DatabaseConnection
from api.utilitiez.responses import (
    duplicate_title,
    duplicate_comment,
)


class Incident:
    """Class that will contain incident objects """

    def __init__(self):
        self.db = DatabaseConnection()

    def create_incident(self, inc_type, **kwargs):
        """Method for inserting a new incident in the database"""
        title = kwargs.get("title")
        comment = kwargs.get("comment")
        location = (kwargs.get("location")[0], kwargs.get("location")[1])
        created_by = kwargs.get("user_id")
        status = "draft"

        # Querry for inserting a new incident record to incidents_db
        sql = (
            "INSERT INTO incidents ("
            "title, comment, location, created_by, status, incident_type"
            ")VALUES ("
            f"'{title}', '{comment}','{location}',"
            f"'{created_by}', '{status}' ,'{inc_type}') returning "
            "incident_id,title as title,"
            "location as location, "
            "created_by as created_by,"
            "status as status, "
            "incident_type as incident_type;"
        )
        self.db.cursor_database.execute(sql)
        new_incident = self.db.cursor_database.fetchone()
        return new_incident

    def insert_images(self, incident_id, images):
        """Function that adds images to the database"""
        for image in images:
            sql = (
                "INSERT INTO incident_images ("
                "incident_id,image_url) VALUES ("
                f"'{incident_id}','{image}');"
            )
            self.db.cursor_database.execute(sql)

    def insert_videos(self, incident_id, videos):
        """Function that adds incident videos to their database"""
        for video in videos:
            sql = (
                "INSERT INTO incident_videos ("
                "incident_id,video_url) VALUES ("
                f"'{incident_id}','{video}');"
            )
            self.db.cursor_database.execute(sql)

    def get_all_incident_records(self, inc_type):
        """Method to allow admin user get all records"""
        if is_admin_user():
            return self.get_all_records(inc_type)
        user_id = str(get_current_identity())

        return self.get_all_records_for_a_specific_user(inc_type, user_id)

    def get_all_records(self, inc_type):
        sql = f"SELECT * FROM incidents WHERE incident_type='{inc_type}';"
        self.db.cursor_database.execute(sql)
        return self.db.cursor_database.fetchall()

    def get_all_records_for_a_specific_user(self, inc_type, user_id):
        """Function for fetching records of a specific user"""
        sql = (
            "SELECT * FROM incidents WHERE "
            f"created_by='{user_id}' AND incident_type='{inc_type}';"
        )
        self.db.cursor_database.execute(sql)

        return self.db.cursor_database.fetchall()

    def get_an_incident_record_(self, inc_type, inc_id):
        inc_id = str(inc_id)
        user_id = get_current_identity()

        record = self.get_incident_by_id_and_type(inc_type, inc_id)
        if record and is_admin_user():
            pass
        elif record and record["created_by"] == user_id:
            pass
        elif record and record["created_by"] != user_id:
            record = {"error": "Access Denied"}
        else:
            record = None
        return record

    def get_incident_by_id_and_type(self, inc_type, inc_id):
        """Function for getting an incident by id and type."""

        sql = (
            f"SELECT * FROM incidents WHERE incident_id='{inc_id}' \
                AND incident_type='{inc_type}';"
        )
        self.db.cursor_database.execute(sql)
        return self.db.cursor_database.fetchone()

    def update_incident_location(self, inc_id, location):
        """Method for updating the location of an incident."""
        location = (location[0], location[1])
        sql = (
            f"UPDATE incidents SET location='{location}' "
            f"WHERE incident_id='{inc_id}' returning incident_id, location;"
        )
        self.db.cursor_database.execute(sql)
        return self.db.cursor_database.fetchone()

    def update_incident_comment(self, inc_id, inc_type, comment):
        """Method for updating a comment of an incident."""
        comment = comment.strip()
        sql = (
            f"UPDATE incidents SET comment='{comment}' "
            f"WHERE incident_id='{inc_id}' returning incident_id, comment;"
        )
        self.db.cursor_database.execute(sql)
        return self.db.cursor_database.fetchone()

    def update_incident_status(self, inc_id, inc_type, status):
        """Method for updating the status of an incident."""
        status = status.strip().lower().capitalize()
        sql = (
            f"UPDATE incidents SET status='{status}' "
            f"WHERE incident_id='{inc_id}' returning incident_id ,status;"
        )
        self.db.cursor_database.execute(sql)
        return self.db.cursor_database.fetchone()

    def delete_incident_record(self, inc_id, inc_type, user_id):
        """Function to delete an incident record."""
        sql = (
            f"DELETE FROM incidents WHERE created_by='{user_id}' "
            f"AND incident_id='{inc_id}' AND incident_type='{inc_type}' returning *;"
        )
        self.db.cursor_database.execute(sql)
        return self.db.cursor_database.fetchone()

    def check_incident_exists(self, title, comment):
        """Making sure that title and comment are unique"""
        incident_exists_query = (
            "SELECT title, comment from incidents where "
            f"title ='{title}' OR comment='{comment}';"
        )
        self.db.cursor_database.execute(incident_exists_query)
        incident_exists = self.db.cursor_database.fetchone()
        error = {}
        # checking existance of either title or comment
        if incident_exists and incident_exists.get("title") == title:
            error["title"] = duplicate_title

        if incident_exists and incident_exists.get("comment") == comment:
            error["comment"] = duplicate_comment
        return error
