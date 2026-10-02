#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
docx(한글판/중국어판 논문·학술지 원고)에서 문단 텍스트를 추출해 UTF-8로 저장한다.
Windows PowerShell 콘솔(cp949)에서 깨지지 않도록 결과는 '파일'로만 쓴다.

사용법:
    python extract_docx.py "<원고.docx>" "<출력_clean.txt>"

출력: 문단 단위로 줄바꿈된 clean.txt (XML 태그 제거).
이 파일에서 CONTENTS(영문 목차)·中文目錄(중문 목차)·編者序/编者序(편집자 서문,
논문별 한 줄 논지)를 찾아 논문별 제목·저자·논지를 매핑한다.
"""
import sys, re, zipfile

def extract(docx_path, out_path):
    with zipfile.ZipFile(docx_path) as z:
        xml = z.read("word/document.xml").decode("utf-8", "ignore")
    paras = re.split(r"</w:p>", xml)
    out = []
    for p in paras:
        ts = re.findall(r"<w:t[^>]*>(.*?)</w:t>", p, re.S)
        txt = "".join(ts)
        # 남은 태그 제거 + 엔티티 정리
        txt = re.sub(r"<[^>]+>", "", txt)
        txt = (txt.replace("&amp;", "&").replace("&lt;", "<")
                  .replace("&gt;", ">").replace("&quot;", '"').replace("&#39;", "'"))
        txt = txt.strip()
        if txt:
            out.append(txt)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print(f"OK: {len(out)} paragraphs -> {out_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: python extract_docx.py <in.docx> <out.txt>")
        sys.exit(1)
    extract(sys.argv[1], sys.argv[2])
