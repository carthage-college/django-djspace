import glob
import tarfile

tar_ball = tarfile.open("/d2/test.tar.gz", mode='w:gz')
path_regex = 'static/files/applications/rocket-launch-team/*/*[A-Z]17_*.pdf'

for name in glob.glob(path_regex):
    path_list = name.split('/')
    phile = path_list[-1]
    tar_ball.add(name, arcname=phile)

tar_ball.close()

