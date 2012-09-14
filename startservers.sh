#!/bin/bash
workon labrad
twistd -n labradnode
python /home/cct/LabRAD/cct/normalstartup.py
sleep 1
python /home/cct/LabRAD/cct/okfpgaservers/pulser/pulser_ok.py &
sleep 1
sleep 1
python /home/cct/LabRAD/cct/dataflowservers/NormalPMTFlow.py &
sleep 2

sleep 5

python /home/cct/clients/CCTGUI.py