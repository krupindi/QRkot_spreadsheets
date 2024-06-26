from datetime import datetime
from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = '%Y/%m/%d %H:%M:%S'
SHEET_TYPE = 'GRID'
SHEET_ID = 0
TITLE = 'Лист1'
ROW_COUNT = 100
COLUMN_COUNT = 11

SPREADSHEET_PROPERTIES = {
    'properties': {'title': '', 'locale': 'ru_RU'},
    'sheets': [
        {'properties': {'sheetType': SHEET_TYPE, 'sheetId': SHEET_ID,
                        'title': TITLE,
                        'gridProperties': {'rowCount': ROW_COUNT,
                                           'columnCount': COLUMN_COUNT}}}]
}

PERMISSIONS_BODY = {'type': 'user', 'role': 'writer',
                    'emailAddress': settings.email}

TABLE_VALUES_HEADER = [
    ['Отчёт от', ''],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]

UPDATE_BODY = {
    'majorDimension': 'ROWS',
    'values': []
}


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = SPREADSHEET_PROPERTIES.copy()
    spreadsheet_body['properties']['title'] = f'Отчёт на {now_date_time}'
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(spreadsheet_id: str,
                               wrapper_services: Aiogoogle) -> None:
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(fileId=spreadsheet_id,
                                   json=PERMISSIONS_BODY,
                                   fields="id")
    )


async def spreadsheets_update_value(spreadsheet_id: str, projects: list,
                                    wrapper_services: Aiogoogle) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = TABLE_VALUES_HEADER.copy()
    table_values[0][1] = now_date_time
    for project in projects:
        duration = project.close_date - project.create_date
        new_row = [project.name, str(duration), project.description]
        table_values.append(new_row)
    update_body = UPDATE_BODY.copy()
    update_body['values'] = table_values
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='A1:C100',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
