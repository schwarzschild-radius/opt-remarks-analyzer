#! /usr/bin/env python3

from urllib import request

def download_file(url, filename):
    request.urlretrieve(url, filename)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Download script")
    parser.add_argument("--dir", type=str, default="./")
    args = parser.parse_args()
    llvm_test_suite_file = "http://download2262.mediafire.com/osyj5gnvkvxg/56kiffbt55s5x91/LLVM+Test+Suite.zip"
    llvm_test_suite_name = args.dir + "/" + "LLVM_Test_Suite.zip"
    llvm_grep_txt_file = "http://download2267.mediafire.com/wa34vg1z6isg/0u7q9ezxxaie088/llvm_opt_remarks_grep.txt"
    llvm_grep_txt_name = args.dir + "/" + "llvm_grep_remarks.txt"
    download_file(llvm_test_suite_file, llvm_test_suite_name)
    download_file(llvm_grep_txt_file, llvm_grep_txt_name)
