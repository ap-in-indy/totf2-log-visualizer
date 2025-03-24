# totf2-log-visualizer
Log visualizer for Thrill of the Fight 2.

1. Connect your Quest to your PC with a USB cable and then put the Quest on and check your notifications for one that says "USB Detected" and click on it. This step is important and should make your Quest show up as an option in your PC's file explorer like a thumb drive would, and sometimes that notification isn't the one on top and is kind of hidden in the list.

2. From your file explorer, access your Quest then go to "Android\data\com.HalfbrickStudios.TheThrilloftheFight2\files\UnityCache\Logs" and you should see a log.txt and previous_log.txt file. You can copy both of those to your desktop or somewhere else on your PC and then you can attach them here.

If you are on Mac OS (depending on versions) you may need to sync files to your phone and pull them off your phone first. For Android, I would recommend OpenMTP as Android File Transfer no longer appears to be maintained.

For running the Python visualizer:

python3
python -m ensurepip --upgrade
pip install pandas
pip instlal matplotlib
python3 visualizer.py

Or condas for virtual environment management:

conda create --name thrillofthefight
conda activate thrillofthefight
conda install pandas
conda install matplotlib
python3 visualizer.py