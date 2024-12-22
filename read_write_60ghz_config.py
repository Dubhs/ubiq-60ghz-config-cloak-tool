import tarfile
import io

def extract_wave_config(config_tar_file):
    config_file = config_tar_file.extractfile("config.json")
    if config_file is not None:
        config = config_file.read().decode('utf-8')
        return config
    return None

def write_wave_config(config, filename):
    with open(filename, 'w') as file:
        file.write(config)

def load_wave_config(filename):
    with open(filename, 'r') as file:
        config = file.read()
        return config

def overwrite_wave_backup(gzip_file_path, config):
    # Extract existing files from the gzip file
    with tarfile.open(gzip_file_path, 'r:gz') as config_tar_file:
        members = config_tar_file.getmembers()
        files = {
            member.name: config_tar_file.extractfile(member).read() for member in members if member.isfile()} # type: ignore

    # Update or add the config.json file
    if config is not None:
        config_bytes = config.encode('utf-8')
        files['config.json'] = config_bytes

    # Create a new tar file in memory
    tar_buffer = io.BytesIO()
    with tarfile.open(fileobj=tar_buffer, mode='w:gz') as tar_file:
        for name, data in files.items():
            tarinfo = tarfile.TarInfo(name)
            tarinfo.size = len(data)
            tar_file.addfile(tarinfo, io.BytesIO(data))

    # Write the new gzipped tar file back to disk
    with open(gzip_file_path, 'wb') as f_out:
        f_out.write(tar_buffer.getvalue())