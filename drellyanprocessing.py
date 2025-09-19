import os
os.getcwd()
os.chdir(r'/home/manhducnmd/manhducnmd/Delphes-3.5.0')

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.font_manager import FontProperties
import pickle

os.environ["PATH"]='/home/manhducnmd/latex/bin/x86_64-linux'
# Enable LaTeX rendering
plt.rcParams['text.usetex'] = False
#plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.family'] = 'sans-serif'

import ROOT
ROOT.gSystem.Load("libDelphes")

try:
    ROOT.gInterpreter.Declare('#include "classes/DelphesClasses.h"')
    ROOT.gInterpreter.Declare('#include "external/ExRootAnalysis/ExRootTreeReader.h"')
except:
    pass

image_track_eta = []
image_track_phi = []
image_track_Pt = []
image_tower_eta = []
image_tower_phi = []
image_tower_Et = []
p4_total_drellyan = []
Mll_total_drellyan = []
DeltaR_total_drellyan = []
DeltaPhi_total_drellyan = []

for i in range(1, 17):
    ROOT.gSystem.Load("libDelphes")
    if i < 10:
        file = ROOT.TFile.Open(f"/home/manhducnmd/manhducnmd/drellyan/Events/run_0{i}/tag_1_delphes_events.root")
    if i >= 10:
        file = ROOT.TFile.Open(f"/home/manhducnmd/manhducnmd/drellyan/Events/run_{i}/tag_1_delphes_events.root")
    tree = file.Get("Delphes")
    print(f"Iteration {i}")

    # Access branches
    towers = ROOT.TClonesArray("Tower")
    tracks = ROOT.TClonesArray("Track")
    muons = ROOT.TClonesArray("Muon")
    electrons = ROOT.TClonesArray("Electron")
    tree.SetBranchAddress("Tower", ROOT.AddressOf(towers))
    tree.SetBranchAddress("Track", ROOT.AddressOf(tracks))
    tree.SetBranchAddress("Muon", ROOT.AddressOf(muons))
    tree.SetBranchAddress("Electron", ROOT.AddressOf(electrons))
    for entry in range(tree.GetEntries()):
        tree.GetEntry(entry)
        if muons.GetEntries() + electrons.GetEntries() >= 2: #Choose events with more than 2 leptons
            Pt_leptons = []
            P4_leptons = []
            if muons.GetEntries() > 0:
                for muon in muons:
                    Pt_leptons.append(muon.P4().Pt())
                    P4_leptons.append(muon.P4())
            if electrons.GetEntries() > 0:
                for electron in electrons:
                    Pt_leptons.append(electron.P4().Pt())
                    P4_leptons.append(electron.P4())
            Pt_leptons = np.array(Pt_leptons)
            P4_leptons = np.array(P4_leptons)
            sorted_indices = np.argsort(Pt_leptons)
            P4_leptons_sorted = P4_leptons[sorted_indices]
            Pt_leptons_sorted = Pt_leptons[sorted_indices]
            Mll = (P4_leptons_sorted[-1] + P4_leptons_sorted[-2]).M()
            Ptll = (P4_leptons_sorted[-1] + P4_leptons_sorted[-2]).Pt()
            Pxll = (P4_leptons_sorted[-1] + P4_leptons_sorted[-2]).Px()
            Pyll = (P4_leptons_sorted[-1] + P4_leptons_sorted[-2]).Py()
            Pzll = (P4_leptons_sorted[-1] + P4_leptons_sorted[-2]).Pz()
            Ell = (P4_leptons_sorted[-1] + P4_leptons_sorted[-2]).E()
            DeltaR = (P4_leptons_sorted[-1]).DeltaR(P4_leptons_sorted[-2])
            DeltaPhi = (P4_leptons_sorted[-1]).DeltaPhi(P4_leptons_sorted[-2])

            condition = (Mll > 20) and (Ptll > 30) and (Pt_leptons_sorted[-1] > 25) and (Pt_leptons_sorted[-2] > 20)
            if len(Pt_leptons_sorted) >= 3:
                condition = condition and (Pt_leptons_sorted[-3] < 10)
            if condition == True:
                Mll_total_drellyan.append(Mll)
                p4_total_drellyan.append([Pxll, Pyll, Pzll, Ell])
                DeltaR_total_drellyan.append(DeltaR)
                DeltaPhi_total_drellyan.append(DeltaPhi)


                constituent_track_eta = []
                constituent_track_phi = []
                constituent_track_Pt = []

                constituent_tower_eta = []
                constituent_tower_phi = []
                constituent_tower_Et = []
                for track in tracks:
                    constituent_track_eta.append(track.Eta)
                    constituent_track_phi.append(track.Phi)
                    constituent_track_Pt.append(track.PT)            
                for tower in towers:
                    constituent_tower_eta.append(tower.Eta)
                    constituent_tower_phi.append(tower.Phi)
                    constituent_tower_Et.append(tower.ET)
                image_track_eta.append(constituent_track_eta)
                image_track_phi.append(constituent_track_phi)
                image_track_Pt.append(constituent_track_Pt)

                image_tower_eta.append(constituent_tower_eta)
                image_tower_phi.append(constituent_tower_phi)
                image_tower_Et.append(constituent_tower_Et)
    print("Done retrieving data")


Mll_total_drellyan = np.array(Mll_total_drellyan)
p4_total_drellyan = np.array(p4_total_drellyan)
DeltaR_total_drellyan = np.array(DeltaR_total_drellyan)
DeltaPhi_total_drellyan = np.array(DeltaPhi_total_drellyan)

print(f"Drellyan number of event pass cut, {len(Mll_total_drellyan)}")
    
image_track_eta = np.array(image_track_eta)
image_track_phi = np.array(image_track_phi)
image_track_Pt = np.array(image_track_Pt)

image_tower_eta = np.array(image_tower_eta)
image_tower_phi = np.array(image_tower_phi)
image_tower_Et = np.array(image_tower_Et)  

with open(f'drellyan_image_track_eta.npy', 'wb') as f:
    np.save(f, image_track_eta)
with open(f'drellyan_image_track_phi.npy', 'wb') as f:
    np.save(f, image_track_phi)
with open(f'drellyan_image_track_Pt.npy', 'wb') as f:
    np.save(f, image_track_Pt)

with open(f'drellyan_image_tower_eta.npy', 'wb') as f:
    np.save(f, image_tower_eta)
with open(f'drellyan_image_tower_phi.npy', 'wb') as f:
    np.save(f, image_tower_phi)
with open(f'drellyan_image_tower_Pt.npy', 'wb') as f:
    np.save(f, image_tower_Et)
    
with open(f'drellyan_image_Mll.npy', 'wb') as f:
    np.save(f, Mll_total_drellyan)  
with open(f'drellyan_image_DeltaR.npy', 'wb') as f:
    np.save(f, DeltaR_total_drellyan)  
with open(f'drellyan_image_DeltaPhi.npy', 'wb') as f:
    np.save(f, DeltaPhi_total_drellyan)  
with open(f'drellyan_image_p4.npy', 'wb') as f:
    np.save(f, p4_total_drellyan)  