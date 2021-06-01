def tja_to_time(tja_name):
    with open(tja_name, 'r') as f:
        note_list = []
        time_list = []
        scroll_list = []
        note_line = [] #當遇到同個小節但是有分行時，額外紀錄音符與時間
        time_line = []
        measure = 4
        scroll = 1
        branch = 0 
        for line in f:
            if line.startswith('BPM'):
                bpm = float(line[4:-1])
                sec_time = 60/bpm #四分音符的時長
                continue
            elif line.startswith('#START'):
                t = 0
                continue
            elif line.startswith('#END'):
                break
            elif line.startswith('#MEASURE'):
                measure = int(line.split('/')[0][-1] / line.split('/')[1][1] * 4)
                continue
            elif line.startswith('#BPMCHANGE'):
                bpm = float(line.split(' ')[1][:-1])
                sec_time = 60/bpm
            elif line.startswith('#SCROLL'):
                scroll = line.split(' ')[1][:-1]
            elif (',' in line) or line[0].isdigit():
                if line[0] == ',':
                    t += sec_time * measure
                    continue
                elif ',' not in line or branch:
                    if ',' in line:
                        branch = 0
                        line_split = line.split(',')[0]
                        for i in line_split:
                            note_line.append(i)
                            time_line.append(sec_time * measure)
                            if i != '0':
                                scroll_list.append(scroll)
                        len_line = len(note_line)
                        for i in range(len(note_line)):
                            note_time = time_line[i] / len_line
                            if note_line[i] != '0':
                                note_list.append(note_line[i])
                                time_list.append(t)
                            t += note_time
                        note_line = []
                        time_line = []
                        continue
                    line_split = line.split(',')[0][:-1]
                    for i in line_split:
                        note_line.append(i)
                        time_line.append(sec_time * measure)
                        if i != '0':
                            scroll_list.append(scroll)
                    branch = 1
                elif not branch:
                    line_split = line.split(',')[0]
                    note_time = sec_time * measure / len(line_split)
                    for i in line_split:
                        if i == '0':
                            t += note_time
                        elif i != '0':
                            time_list.append(t)
                            note_list.append(i)
                            scroll_list.append(scroll)
                            t += note_time
            #暫時略過浮動BPM與火燒區
    return time_list, note_list, scroll_list