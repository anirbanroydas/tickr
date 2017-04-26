from doubles import allow, expect, ClassDouble, allow_constructor
import pytest




def test_get_mainpage(client):
	page = client.get("/")
	assert page.status_code == 200


	


if __name__ == '__main__':
	# unittest.main()
	pytest.main()
