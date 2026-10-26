import json
import math

QKV = json.load(open("qkv.json"))
Q, K, V = QKV["Q"], QKV["K"], QKV["V"]


def softmax(xs):
    return xs


def attention(Q, K, V, causal=False):
    return [], []


def most_attended(weights):
    return []
