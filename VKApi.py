from urllib.parse import urlencode
import requests
import time

token = "fe27813f7baa5aa43a6edba5ba21a48b68e75ebfe9a1e3ada18914350af19222a5d44fab1aa66268086bd"
params = {
  "access_token": token,
  "v": 5.103
}

class User:
  # Initialiazation class
  def __init__(self, user_id):
    self.user_id = user_id
    self.count_friends = 0
    self.error = 0

    fio = self.get_fio()
    # print(fio)
    if fio == None:
      print(f"Аккаунт ВК с id = {user_id} не определен.")
      self.error = -1

  # Get list of friends of user if didn't it
  def get_friends_if_need(self):
    if self.count_friends <= 0:
      self.get_id_friends()

  # Get value by key=field_name from dictionary
  def get_field_of_response(self, response_json, field_name):
    try:
      return response_json[field_name]
    except KeyError:
      print(f"Не найден ключ \"{field_name}\" в ответе {response_json}")
    except TypeError:
      print(f"Входные данные типа {type(response_json)}, а ожидается тип {type(dict())}")

  # Override operation "&"
  def __and__(self, other):
    return self.get_common_friends(other)

  # Print instance of class
  def __str__(self):
    return f"https://vk.com/id{self.user_id}"

  # Detect a status of user
  def get_fio(self):
    """

    (None) -> str

    Function gets FIO of user VK

    """
    if 'self.last_name' in locals() and 'self.first_name' in locals():
      return f"{self.last_name} {self.first_name}"

    params_here = params.copy()
    params_here["user_ids"] = self.user_id

    response = requests.get('https://api.vk.com/method/users.get', params_here)
    response_json = response.json()
    # print(response_json)
    info_json_list = self.get_field_of_response(response_json, 'response')
    if info_json_list == None:
      return

    if len(info_json_list) <= 0:
      return

    info_json = info_json_list[0]

    self.last_name = self.get_field_of_response(info_json, 'last_name')
    if self.last_name == None or self.last_name == 'DELETED':
      return

    self.first_name = self.get_field_of_response(info_json, 'first_name')
    if self.first_name == None or self.first_name == 'DELETED':
      return

    return f"{self.last_name} {self.first_name}"

  # Detect a status of user
  def get_status(self):
    """

    (None) -> str

    Function gets status of user VK

    """

    if 'self.status' in locals():
      return self.status

    params_here = params.copy()
    params_here["user_id"] = self.user_id

    response = requests.get('https://api.vk.com/method/status.get', params_here)
    info_json = self.get_field_of_response(response.json(), 'response')
    if info_json == None:
      return

    self.status = self.get_field_of_response(info_json, 'text')
    if self.status == None:
      return

    return self.status

  # Get list of friends of user
  def get_id_friends(self):
    """

    (None) -> list

    Function gets list of id friends of user VK

    """

    if 'self.friends' in locals():
      return self.friends

    params_here = params.copy()
    params_here["user_id"] = self.user_id
    params_here["order"] = "hints"

    response = requests.get('https://api.vk.com/method/friends.get', params_here)
    response_json = response.json()

    info_json = self.get_field_of_response(response_json, 'response')
    if info_json == None:
      return

    self.count_friends = self.get_field_of_response(info_json, 'count')
    if self.count_friends == None:
      return

    self.friends = self.get_field_of_response(info_json, 'items')
    if self.friends == None:
      return

    return self.friends

  # Get list of common friends of user=self and user=other
  def get_common_friends(self, other):
    """

    (instance of class User) -> list

    Function gets common friends in list of objects of User

    """

    if type(other) != User:
      print(f"Входные данные типа {type(other)}, а ожидается тип {type(self)}")
      return

    self.get_friends_if_need()
    other.get_friends_if_need()

    # Convertions to sets from lists
    self_friends = set(self.friends)
    other_friends = set(other.friends)

    # Getting common friends equals intersection of sets
    common_friends_list = list(self_friends.intersection(other_friends))

    common_friends = []
    for user_id in common_friends_list:
      user_friend = User(user_id)
      common_friends.append(user_friend)

    return common_friends

def auth():
  """

  (None) -> None

  Function helps getting token

  """

  OAUTH_URL = "https://oauth.vk.com/authorize"
  OAUTH_PARAMS = {
    "client_id": 7238600,
    # "redirect_uri": dfgdfgdf,
    "display": "page",
    "response_type": "token",
    "scope": "status, friends"
  }

  print("?".join(
    (OAUTH_URL, urlencode(OAUTH_PARAMS)))
  )

def main():
  """

  (None) -> None

  Main function describe main functionality

  """

  # Made it for getting token
  # auth()

  user1 = User("5521318")
  if user1.error == -1:
    print(f"Выход из программы.")
    return

  # because error appeared: many requests per second
  time.sleep(1)

  user2 = User("201983912")
  if user2.error == -1:
    print(f"Выход из программы.")
    return

  # Test method get_common_friends
  # common = user1.get_common_friends(user2)
  common = user1 & user2
  if len(common) > 0:
    print(f"Адреса страниц общих друзей у пользователей ВК \"{user1.get_fio()}\" и \"{user2.get_fio()}\":")
    for user in enumerate(common, 1):
      print(f"{user[0]}. {user[1]}")

# Point of enter to program
main()

