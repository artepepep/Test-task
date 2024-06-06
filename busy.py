busy = [
    {
        'start' : '10:30',
        'stop' : '10:50'
    },
    {
        'start': '18:40',
        'stop' : '18:50'
    },
    {
        'start' : '14:40',
        'stop' : '15:50',
    },
    {
        'start' : '16:40',
        'stop' : '17:20'
    },
    {
        'start' : '20:05',
        'stop' : '20:20'
    }
]


def convert_hm_to_m(hm: str) -> int:
    """ Converts (hours:minutes) type to minutes """
    hm_list = hm.split(":")
    return int(hm_list[0]) * 60 + int(hm_list[1])


def convert_m_to_hm(m: int) -> str:
    """ Converts minutes to (hours:minutes) type """

    if m > 1440:
        raise ValueError(f'One day have less than {m} minutes, pls enter number from 0 to 1440')
    h = m // 60
    minutes = m % 60
    return f"{h}:{minutes:02d}"


def get_free_time_dict(start_of_the_work: str, end_of_the_work: str, lesson_duration: int, busy_dict: dict) -> dict:
    """ Returns a dictionary depending on: start of the day of your work graffic, end of the day of your work graffic, """
    """ duration of your lesson and dictionary of your busy timelines """
    if convert_hm_to_m(start_of_the_work) >= convert_hm_to_m(end_of_the_work):
        raise ValueError('Variable "end_of_the_work" need to be later than variable "start_of_the_work"')
    if lesson_duration >= convert_hm_to_m(end_of_the_work) - convert_hm_to_m(start_of_the_work):
        raise ValueError('Variable "lesson_duration" need to be less than length of the day')
    busy_list = []
    for hm in busy_dict:
        busy_list.append([convert_hm_to_m(hm['start']), convert_hm_to_m(hm['stop'])])
    busy_list = sorted(busy_list)

    start = convert_hm_to_m(start_of_the_work)
    end = convert_hm_to_m(end_of_the_work)
    curr_start = start
    free_intervals = []
    for time in busy_list:
        busy_start, busy_end = time

        while curr_start + lesson_duration <= busy_start:
            free_intervals.append({'start': convert_m_to_hm(curr_start), 'stop': convert_m_to_hm(curr_start + lesson_duration)})
            curr_start += lesson_duration

        if curr_start < busy_end:
            curr_start = busy_end
        
    while curr_start + lesson_duration <= end:
        free_intervals.append({'start': convert_m_to_hm(curr_start), 'stop': convert_m_to_hm(curr_start + lesson_duration)})
        curr_start += lesson_duration
    
    return free_intervals

print(get_free_time_dict('10:00', '22:00', 30, busy)) # Example