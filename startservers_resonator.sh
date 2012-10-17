#!/bin/bash
python /home/resonator/labrad/cct/okfpgaservers/pulser/pulser_ok.py &
sleep 1
python /home/resonator/labrad/cct/dataflowservers/NormalPMTFlow.py &
sleep 2
python /home/resonator/labrad/cct/DAC/CCTDAC_PULSER.py &
sleep 3
python /home/resonator/labrad/cct/datavault/dvascii.py &
#python /home/resonator/labrad/cct/normalstartup.py &

