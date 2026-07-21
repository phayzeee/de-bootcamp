# // 1
# data class User(val id: Int, val name: String, val email: String? = null)
# // 2
# val len = user?.email?.length ?: 0
# // 3
# val label = when (code) { 200 -> "ok"; 404 -> "missing"; in 500..599 -> "server"; else -> "other" }
# // 4
# val squares = (1..10).filter { it % 2 == 0 }.map { it * it }
# // 5
# val line = "User ${user.name} has ${items.size} items: ${items.joinToString(", ")}"
# // 6
# fun String.initials() = split(" ").joinToString("") { it.first().uppercase() }
# // 7
# val grouped = orders.groupBy { it.city }        // orders: List<Order(city, amount)>
# // 8
# object Config { val retries = 3 }

from dataclasses import dataclass



@dataclass
class User:
    id: int
    name: str
    email: str | None = None

def label(status):
    match status:
        case 200:
            return 'OK'
        case 400:
            return 'missing'
        case x if x in range(500,600):
            return 'server'
        case _:
            return 'other'

#4
def squares():
        return [x * x for x in range(1, 11) if x % 2 == 0]

#6
def initials(s: str) -> str:
    return "".join(word[0].upper() for word in s.split(" "))

#8
class Config:
    retries = 3


if __name__ == "__main__":
    user = User(id=1, name="Phayzee", email=None)
    print(user)

    length = len(user.email) if user.email is not None else 0
    print(length)

    print(label(510))

    items = ["book", "pen", "bag"]
    line = f"User {user.name} has {len(items)} items: {', '.join(items)}"
    print(line)

    print(squares())
    print(initials("John Doe"))
    print(Config.retries)