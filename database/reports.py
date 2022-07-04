from sqlmodel import Session

from . import Report


def create_report(session: Session, data: dict) -> Report:
    report_type = data['type']
    report_text = data['message']
    file_url = data['file_url']
    user_id = data['user_id']
    report = Report(type=report_type,
                    text=report_text,
                    photos=file_url,
                    user_id=user_id)
    session.add(report)
    session.commit()
    session.refresh(report)
    return report
