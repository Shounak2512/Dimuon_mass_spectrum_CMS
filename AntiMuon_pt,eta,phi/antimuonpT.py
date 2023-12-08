import ROOT

# Enable multi-threading
# The default here is set to a single thread. You can choose the number of threads based on your system.
ROOT.ROOT.EnableImplicitMT()

# Create dataframe from NanoAOD files
df = ROOT.RDataFrame("Events", "Run2012BC_DoubleMuParked_Muons.root")

# Select events with exactly two muons
df_2mu = df.Filter("nMuon == 2", "Events with exactly two muons")

# Select events with two muons of opposite charge
df_os = df_2mu.Filter("Muon_charge[0] != Muon_charge[1]", "Muons with opposite charge")

df_final = df_os.Define("good_idx", "Muon_charge==1").Define("AntiMuon_pT", "Muon_pt[good_idx]")

# Book histogram of dimuon mass spectrum
bins = 500 # Number of bins in the histogram
low = 0.25 # Lower edge of the histogram
up = 100 # Upper edge of the histogram
hist = df_final.Histo1D(ROOT.RDF.TH1DModel("", "Anti-Muon pT", bins, low, up), "AntiMuon_pT")


# Create canvas for plotting
ROOT.gStyle.SetTextFont(42)
c = ROOT.TCanvas("c", "Anti Muon pT", 800, 700)


hist.GetXaxis().SetTitle("pT (GeV)")
hist.GetXaxis().SetTitleSize(0.04)
hist.GetYaxis().SetTitle("N_{Events}")
hist.GetYaxis().SetTitleSize(0.04)
hist.Draw()

#To stop the script from closing
input("Press enter to save plot")

#Save plot
c.SaveAs("antimuonphi.pdf")


