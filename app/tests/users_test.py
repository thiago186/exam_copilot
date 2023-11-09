from datetime import datetime

from schemas.users import User

mockUser = User(
    user_id = "26dadba8-6473-41b6-9942-823e49a027ec",
    email="thiago@test.com.br",
    username="thiago",
    hashed_password="$2b$12$TfRVPNQ2lNq8NOcP8rw0v.rxcTMZ/PdKOl9nX3gWbNL41r4pDRG6m",
    current_plan="basic",
    plan_due_date=datetime(2023,12,30),
    create_at=datetime(2023,7,11),
    active=True
)

    # """This class defines the schema for the User model."""
    # user_id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    # email: str
    # username: str
    # hashed_password: str
    # current_plan: str
    # plan_due_date: Optional[datetime]
    # created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    # active: bool = Field(default=True
                         
@pytest.fixture(name="session", scope="function")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session 

def test_create_user(session):
    test_email = "test@example.com"
    test_username = "testuser"
    test_password = "securepassword123"
    test_plan = "basic"

    user = User(email=test_email, username=test_username, current_plan=test_plan)
    user.set_password(test_password)
    session.add(user)
    session.commit()
    session.refresh(user)

    assert user.user_id is not None
    assert user.email == test_email
    assert user.username == test_username
    assert user.verify_password(test_password) 
    assert user.current_plan == test_plan
    assert user.active is True
    assert user.created_at is not None
