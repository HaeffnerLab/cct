#!/bin/bash
cd /home/cct/LabRAD/cct/okfpgaservers/pulser.old/
python pulser_ok.py &
sleep 1
python /home/cct/LabRAD/cct/dataflowservers/NormalPMTFlow.py &
sleep 2
cd /home/cct/LabRAD/cct/DAC/
python CCTDAC_PULSER.py &
sleep 3
python /home/cct/LabRAD/cct/normalstartup.py &

