import os


def parse(filename, separator=' ', collapsed_head=True):
    config = {}
    if os.path.exists(filename):
        for file_line in open(filename, 'r'):
            file_line = file_line.strip()
            comment_pos = file_line.find('#')
            if comment_pos == 0:
                continue
            if comment_pos > 0:
                file_line = file_line[:comment_pos-1]
            items = file_line.split(separator)
            count = len(items)
            if count == 2:
                config[items[0]] = items[1]
            elif count > 2:
                if collapsed_head:
                    config[' '.join(items[:count-1])] = items[count-1]
                else:
                    config[items[0]] = items[1:]
    return config
