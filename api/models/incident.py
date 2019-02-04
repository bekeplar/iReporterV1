from api.helpers.auth_token import get_current_identity, is_admin_user
from database.db import DatabaseConnection


class Incident:
    def __init__(self):
        self.db = DatabaseConnection('Database_url')

    def insert_incident(self, inc_type="red-flag", **kwargs):
        title = kwargs.get("title")
        comment = kwargs.get("comment")
        location = (kwargs.get("location")[0], kwargs.get("location")[1])
        created_by = kwargs.get("user_id")
        images = kwargs.get("images")
        videos = kwargs.get("videos")
        sql = (
            "INSERT INTO public.incidents ("
            "title, comment, location, created_by, type"
            ")VALUES ("
            f"'{title}', '{comment}','{location}',"
            f"'{created_by}', '{inc_type}') returning id;"
        )
        self.db.cursor.execute(sql)
        last_insert_id = self.db.cursor.fetchone()
        new_incident_id = last_insert_id.get("id")
        self.insert_images(new_incident_id, images)
        self.insert_videos(new_incident_id, videos)
        return self.get_incident_by_id(new_incident_id)

    def insert_images(self, incident_id, images):
        for image in images:
            sql = (
                "INSERT INTO public.incident_images ("
                "incident_id,image_url) VALUES ("
                f"'{incident_id}','{image}');"
            )
            self.db.cursor.execute(sql)

    def insert_videos(self, incident_id, videos):
        for video in videos:
            sql = (
                "INSERT INTO public.incident_videos ("
                "incident_id,video_url) VALUES ("
                f"'{incident_id}','{video}');"
            )
            self.db.cursor.execute(sql)

    def get_all_incident_records(self, inc_type):
        if is_admin_user():  # if user is admin
            return self.get_all_records(inc_type)
        user_id = str(get_current_identity())

        return self.get_all_records_for_a_specific_user(inc_type, user_id)

    def get_all_records(self, inc_type):
        sql = f"SELECT * FROM incident_view WHERE type='{inc_type}';"
        self.db.cursor.execute(sql)
        return self.db.cursor.fetchall()

    def get_all_records_for_a_specific_user(self, inc_type, user_id):
        sql = (
            "SELECT * FROM incident_view WHERE "
            f"created_by='{user_id}' AND type='{inc_type}';"
        )
        self.db.cursor.execute(sql)

        return self.db.cursor.fetchall()

    def get_an_incident_record_(self, inc_type, inc_id):
        inc_id = str(inc_id)
        user_id = get_current_identity()

        record = self.get_incident_by_id_and_type(inc_type, inc_id)
        if record and is_admin_user():
            pass
        elif record and record["created_by"] == user_id:
            pass
        elif record and record["created_by"] != user_id:
            record = {"error": "You're not Authorized to access this resource"}
        else:
            record = None
        return record

    def get_incident_by_id(self, inc_id):

        sql = f"SELECT * FROM public.incident_view " f"WHERE id='{inc_id}';"
        self.db.cursor.execute(sql)
        return self.db.cursor.fetchone()

    def get_incident_by_id_and_type(self, inc_type, inc_id):

        sql = (
            f"SELECT * FROM public.incident_view "
            f"WHERE id='{inc_id}' AND type='{inc_type}';"
        )
        self.db.cursor.execute(sql)
        return self.db.cursor.fetchone()

    def update_incident_location(self, inc_id, location):
        location = (location[0], location[1])
        sql = (
            f"UPDATE incidents SET location='{location}' "
            f"WHERE id='{inc_id}' returning id,location;"
        )
        self.db.cursor.execute(sql)
        return self.db.cursor.fetchone()

    def update_incident_comment(self, inc_id, inc_type, comment):
        comment = comment.strip()
        sql = (
            f"UPDATE incidents SET comment='{comment}' "
            f"WHERE id='{inc_id}' returning id,comment;"
        )
        self.db.cursor.execute(sql)
        return self.db.cursor.fetchone()

    def update_incident_status(self, inc_id, inc_type, status):
        status = status.strip().lower().capitalize()
        sql = (
            f"UPDATE incidents SET status='{status}' "
            f"WHERE id='{inc_id}' returning id,status;"
        )
        self.db.cursor.execute(sql)
        return self.db.cursor.fetchone()

    def delete_incident_record(self, inc_id, inc_type, user_id):
        sql = (
            f"DELETE FROM incidents WHERE created_by='{user_id}' "
            f"AND id='{inc_id}' AND type='{inc_type}' returning *;"
        )
        self.db.cursor.execute(sql)

        return self.db.cursor.fetchone()
