import time
import fire_base


class Diary:
    title = None
    feeling = None
    text = None

    def create_diary(self):
        data = fire_base.create('diaries', {'created': True})
        return data

    def show_entries(self, diary_id: str):
        diary_data = fire_base.get_by_id('diaries', diary_id)
        if diary_data is None:
            return False

        return diary_data

    def insert_into_diary(self, diary_id: str):
        diary_data = self.show_entries(diary_id)
        if not diary_data:
            return False

        entry_key = int(time.time() * 1000)
        diary_data[str(entry_key)] = {
            'title': self.title,
            'feeling': self.feeling,
            'text': self.text
        }
        fire_base.update('diaries', diary_id, diary_data)
        return True

    def find_entry_by_id(self, diary_id: str, entry_id: str):
        diary_data = self.show_entries(diary_id)
        if entry_id in list(diary_data.keys()):
            return diary_data[entry_id]

        return None

    def update_entry(self, diary_id: str, entry_id: str, data: dict):
        diary_data = self.show_entries(diary_id)
        if entry_id in list(diary_data.keys()):
            diary_data[entry_id] = data
            fire_base.update('diaries', diary_id, diary_data)
            return True

        return False

    def delete_entry(self, diary_id: str, entry_id: str):
        diary_data = self.show_entries(diary_id)
        if entry_id in list(diary_data.keys()):
            del (diary_data[entry_id])
            fire_base.update('diaries', diary_id, diary_data)
            return True

        return False
