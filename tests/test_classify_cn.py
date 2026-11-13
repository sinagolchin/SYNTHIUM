"""Tests for the Chinese tenor classifier."""
from synthium.blind import classify_cn

def test_affirm():
    t = "......本院认为......裁定如下:驳回上诉,维持原判。审判长......"
    assert classify_cn(t)[0] == "CLEAN_AFFIRM"

def test_reverse_remand():
    t = "......判决如下:一、撤销原判;二、发回重审。"
    assert classify_cn(t)[0] == "REVERSED"

def test_modify():
    t = "......判决如下:一、维持原判第一项;二、改判被告人有期徒刑三年。"
    assert classify_cn(t)[0] == "MODIFIED"

def test_ambiguous():
    assert classify_cn("本案正在审理之中。")[0] == "AMBIGUOUS"
