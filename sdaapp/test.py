from subprocess import Popen, PIPE, CalledProcessError
import tarfile

def main():
    export_args = ['sudo', 'docker', 'cp', 'sandbox1:/outputs/.', '-']
    exporter = Popen(export_args, stdout=PIPE)
    tar_file = tarfile.open(fileobj=exporter.stdout, mode='r|')
    tar_file.extractall('.', members=exclude_root(tar_file))
    exporter.wait()
    if exporter.returncode:
        raise CalledProcessError(exporter.returncode, export_args)

def exclude_root(tarinfos):
    print('\nOutputs:')
    for tarinfo in tarinfos:
        if tarinfo.name != '.':
            assert tarinfo.name.startswith('./'), tarinfo.name
            print(tarinfo.name[2:])
            tarinfo.mode |= 0o600
            yield tarinfo

main()
