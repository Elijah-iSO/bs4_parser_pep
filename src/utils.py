import logging

from bs4 import BeautifulSoup
from requests import RequestException

from constants import EXPECTED_STATUS
from exceptions import ParserFindTagException


def get_response(session, url):
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except RequestException:
        logging.exception(
            f'Возникла ошибка при загрузке страницы {url}',
            stack_info=True
        )


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs}'
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag


def get_status(session, pep_link):
    response = get_response(session, pep_link)
    if response is None:
        return
    soup = BeautifulSoup(response.text, 'lxml')
    dl_tag = find_tag(soup, 'dl')
    dt_tag = dl_tag.find_all('dt')
    status = dl_tag.find(string='Status')

    for tag in dt_tag:
        if status in tag.text:
            return tag.find_next_sibling('dd').text


def compare_statuses(preview_status, inner_status, pep_link):
    if inner_status not in preview_status:
        error_msg = (
            'Несовпадающие статусы:\n'
            f'{pep_link}\n'
            f'Статус в карточке: {inner_status}\n'
            f'Ожидаемые статусы: {preview_status}\n'
        )
        logging.info(error_msg)


def get_results(status_counter):
    results = [('Cтатус', 'Количество')]
    status_counter['Total'] = sum(status_counter.values())

    for status, amount in status_counter.items():
        results.append((status, amount))

    return results
