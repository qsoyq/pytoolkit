from pytoolkit.scripts.laiye.laiye_web_message_route_tsingtao import replace_host_and_port


def test_replace_host_and_port():
    url = "http://example.org/path/to/api"
    assert replace_host_and_port(url) == 'https://chatai.tsingtao.com.cn:443/path/to/api'
