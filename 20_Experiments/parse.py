def parse_log(file_path):
    with open(file_path, 'r', encoding='utf-8') as fi:
        line = fi.readline()

        fo = open("access_log_jul95.csv", 'w', encoding='utf-8')
        fo.write("IP|DATE|TYPE|URI|RESULT|SIZE\n")

        cnt = 0

        while line:
            if '|' in line:
                line = fi.readline()
                continue

            parts = line.split(' ')

            try:
                items = {
                    "ip": parts[0],
                    "date": parts[3].replace('[', ''),
                    "type": parts[5].replace('"', ''),
                    "uri": parts[6],
                    "result": parts[-2],
                    "size": parts[-1].replace("\n", ""),
                }
            except:
                print("Error Line type1: %d" % cnt)
                print(parts)

            cnt += 1

            if cnt % 1000 == 0:
                print(cnt)

            # print(items)

            wline = "%(ip)s|%(date)s|%(type)s|%(uri)s|%(result)s|%(size)s\n" % items
            fo.write(wline)

            try:
                line = fi.readline()
            except:
                print(parts)
                print("Error Line type2: %d" % cnt)
                continue


        fo.close()

    return True

file = "access_log_jul95"
parse_log(file)
