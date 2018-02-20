from pys3viewercli.CommandLineHelper import CommandLineHelper


def main():
    access_key_id = input('Enter access_key_id:');
    secret_access_key = input('Enter secret_access_key:');
    command_line_helper = CommandLineHelper()
    result = command_line_helper.build_user_session(access_key_id, secret_access_key)
    print(result);


if __name__ == '__main__':
   main()
