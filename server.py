from typing import Type

from pydantic import ValidationError

from flask import Flask, jsonify, request
from flask.views import MethodView
from models import Announcements, Session
from schema import CreateAnnouncement

app = Flask('app')


def validate(json_data, model_class: Type[CreateAnnouncement]):
    try:
        model_item = model_class(**json_data)
        return model_item.dict(exclude_none=True)
    except ValidationError as err:
        raise HttpError(400, err.errors())


class HttpError(Exception):

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({'status': 'error', 'message': error.message})
    response.status_code = error.status_code
    return response


def get_announcement(id: int, session: Session):
    announcement = session.get(Announcements, id)
    if announcement is None:
        raise HttpError(404, message='announcement not found')
    return announcement


class AnnouncementsView(MethodView):

    def get(self, id: int):
        with Session() as session:
            announcement = get_announcement(id, session)
            return jsonify({
                'id': announcement.id,
                'header': announcement.header,
                'description': announcement.description,
                'user': announcement.user,
                'create_date': announcement.create_date.isoformat()
            })

    def post(self):
        json_data = validate(request.json, CreateAnnouncement)
        with Session() as session:
            new_announcement = Announcements(**json_data)
            session.add(new_announcement)
            session.commit()
            return jsonify({
                'id': new_announcement.id
            })

    def delete(self, id: int):
        with Session() as session:
            announcement = get_announcement(id, session)
            session.delete(announcement)
            session.commit()
            return jsonify({
                'status': 'success'
            })


app.add_url_rule('/announcement/<int:id>',
                 view_func=AnnouncementsView.as_view('announcement'),
                 methods=['GET', 'DELETE'])
app.add_url_rule('/announcement',
                 view_func=AnnouncementsView.as_view('announcement_new'),
                 methods=['POST', ])


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
