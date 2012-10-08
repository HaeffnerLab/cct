#!/bin/bash
cd /home/resonator/labrad/cct/okfpgaservers/pulser/
python pulser_ok.py &
sleep 1
python /home/resonator/labrad/cct/dataflowservers/NormalPMTFlow.py &
sleep 2
cd /home/resonator/labrad/cct/DAC/
python CCTDAC_PULSER.py &
sleep 3
cd /home/resonator/labrad/cct/datavault/dvascii.py &
#python /home/resonator/labrad/cct/normalstartup.py &

