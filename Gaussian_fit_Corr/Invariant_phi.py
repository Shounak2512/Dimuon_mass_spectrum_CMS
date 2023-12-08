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
ROOT.gInterpreter.Declare(
"""
using namespace ROOT::VecOps;
float computeInvariantMass(RVec<float>& pt, RVec<float>& eta, RVec<float>& phi, RVec<float>& mass) {
    ROOT::Math::PtEtaPhiMVector m1(pt[0], eta[0], phi[0], mass[0]);
    ROOT::Math::PtEtaPhiMVector m2(pt[1], eta[1], phi[1], mass[1]);
    return (m1 + m2).mass();
}
""")
df_mass = df_os.Define("Dimuon_mass", "computeInvariantMass(Muon_pt, Muon_eta, Muon_phi, Muon_mass)")

# Book histogram of dimuon mass spectrum
bins = 100 # Number of bins in the histogram
low = 0.97# Lower edge of the histogram
up = 1.05 # Upper edge of the histogram
hist = df_mass.Histo1D(ROOT.RDF.TH1DModel("", "Phi", bins, low, up), "Dimuon_mass")
fit=ROOT.TF1("fit","gaus",1.002,1.035)
fit.FixParameter(0,3.3333e+03)
fit.FixParameter(1,1.01834)
fit.FixParameter(2,1.77111e-02)
hist.Fit("fit","B,R")
#Constant[0],Mean[1],Sigma[2]



# Create canvas for plotting
ROOT.gStyle.SetOptStat(1)
ROOT.gStyle.SetOptFit(1)
ROOT.gStyle.SetTextFont(42)
c = ROOT.TCanvas("c", "Main Canvas", 800, 700)
c.SetLogx()
c.SetLogy()

# Draw histogram
hist.GetXaxis().SetTitle("m_{#mu#mu} (GeV)")
hist.GetXaxis().SetTitleSize(0.04)
hist.GetYaxis().SetTitle("N_{Events}")
hist.GetYaxis().SetTitleSize(0.04)
hist.Draw()

# Draw labels
label = ROOT.TLatex()
label.SetNDC(True)
label.SetTextAlign(11)
label.SetTextSize(0.04)
label.DrawLatex(0.10, 0.92, "#bf{CMS Open Data}")
label.SetTextAlign(31)
label.DrawLatex(0.90, 0.92, "#sqrt{s} = 8 TeV, L_{int} = 11.6 fb^{-1}")

# Save plot
c.SaveAs("Phi.pdf")

input("Press enter to close plot.")

