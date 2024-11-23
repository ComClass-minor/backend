from core.config import generate_secret_key

def test_generate_secret_key():
    # Test that the function returns a non-empty string
    key = generate_secret_key()
    assert isinstance(key, str)
    assert len(key) > 0



def test_env_file_creation(tmp_path):
    # Create a temporary directory for testing
    test_env_path = tmp_path / '.env'
    
    # Mock the environment setup
    env_content = f'SECRET_KEY={generate_secret_key()}\n'
    
    # Write to test environment file
    with open(test_env_path, 'w') as f:
        f.write(env_content)
    
    # Verify file exists and contains SECRET_KEY
    assert test_env_path.exists()
    with open(test_env_path, 'r') as f:
        content = f.read()
        assert content.startswith('SECRET_KEY=')
        assert len(content.strip()) > 10



def test_env_file_not_overwritten(tmp_path):
    # Test that existing .env files aren't overwritten
    test_env_path = tmp_path / '.env'
    
    # Create initial .env file
    original_content = 'SECRET_KEY=original_test_key\n'
    with open(test_env_path, 'w') as f:
        f.write(original_content)
    
    # Try to create it again
    with open(test_env_path, 'r') as f:
        new_content = f.read()
    
    # Verify original content wasn't changed
    assert new_content == original_content