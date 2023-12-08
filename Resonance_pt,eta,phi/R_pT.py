import ROOT

# Enable multi-threading
ROOT.ROOT.EnableImplicitMT()

# Create dataframe from NanoAOD files
df = ROOT.RDataFrame("Events", "Run2012BC_DoubleMuParked_Muons.root")

# Select events with exactly two muons
df_2mu = df.Filter("nMuon == 2", "Events with exactly two muons")

# Select events with two muons of opposite charge
df_os = df_2mu.Filter("Muon_charge[0] != Muon_charge[1]", "Muons with opposite charge")

# Compute invariant mass of the dimuon system
# The following code just-in-time compiles the C++ function to compute
# the invariant mass, so that the function can be called in the Define node of
# the ROOT dataframe.
ROOT.gInterpreter.Declare(
"""
using namespace ROOT::VecOps;
float pT(RVec<float>& pt, RVec<float>& eta, RVec<float>& phi, RVec<float>& mass) {
    ROOT::Math::PtEtaPhiMVector m1(pt[0], eta[0], phi[0], mass[0]);
    ROOT::Math::PtEtaPhiMVector m2(pt[1], eta[1], phi[1], mass[1]);
    return (m1 + m2).pt();
}
""")
df_mass = df_os.Define("Resonance_pT", "pT(Muon_pt, Muon_eta, Muon_phi, Muon_mass)")

# Book histogram of dimuon mass spectrum
bins = 500 # Number of bins in the histogram
low = -1 # Lower edge of the histogram
up = 250 # Upper edge of the histogram
hist = df_mass.Histo1D(ROOT.RDF.TH1DModel("", "Transverse Momentum of Resonances", bins, low, up), "Resonance_pT")

# Request cut-flow report
report = df_mass.Report()

# Create canvas for plotting
ROOT.gStyle.SetTextFont(42)
c = ROOT.TCanvas("c", "", 800, 700)

# Draw histogram
hist.GetXaxis().SetTitle("pT (GeV)")
hist.GetXaxis().SetTitleSize(0.04)
hist.GetYaxis().SetTitle("N_{Events}")
hist.GetYaxis().SetTitleSize(0.04)
hist.Draw()


# Save plot
c.SaveAs("Resonance_pT.pdf")

input()
