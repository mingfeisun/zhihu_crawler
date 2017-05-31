import json_lines as jsl

def view_jsonlines():
    with open("zhihu_live.jl") as f_in:
        print f_in.readline()


if __name__ == "__main__":
    print "hello"
    view_jsonlines()
