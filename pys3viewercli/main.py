import click
from pys3viewercli import Spinner
from pys3viewercli import CommandLineHelper


@click.command()
@click.option('--access_key_id', prompt='Enter access_key_id: ', help='Input AWS access_key_id to access s3 bucket:')
@click.option('--secret_access_key', prompt='Enter secret_access_key: ',
              help='Input AWS secret_access_key to access s3 bucket.')
@click.option('--tree', default='N', help='Input AWS access_key_id to access s3 bucket:')
def main(access_key_id, secret_access_key, tree):
    """Main used to list all the s3 buckets and corresponding details/files accessible by a user

    Args:
        access_key_id: AWS access_key_id to access s3 bucket.
        secret_access_key: AWS secret_access_key to access s3 bucket.
        tree: use 'Y' if need to print the tree-view listing of all files in buckets accessible by user

    Returns:
        Command line output of the files and directory structure from all S3 buckets.
    """
    command_line_helper = CommandLineHelper.CommandLineHelper()
    # spinner = Spinner()
    # spinner.start()
    if tree is 'Y':
        result = command_line_helper.list_all_files_in_all_buckets_for_user(access_key_id, secret_access_key)
    else:
        result = command_line_helper.list_bucket_info_for_user(access_key_id, secret_access_key)
    # spinner.stop()
    print(result)


if __name__ == '__main__':
    main()
