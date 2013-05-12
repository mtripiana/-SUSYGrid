#include <iostream>
#include <fstream>
#include <string>
using namespace std;

void SetStyle()
{
  gStyle->SetPalette(1);
  gStyle->SetFrameFillColor(0);
  gStyle->SetFrameBorderSize(0);
  gStyle->SetFrameBorderMode(0);
  //  gStyle->SetFillColor(0);
  gStyle->SetCanvasColor(0);
  gStyle->SetOptStat(0);
  gStyle->SetTitleBorderSize(0);
  gStyle->SetTitleFillColor(0);
  gStyle->SetTextFont(42);
  gStyle->SetLabelFont(42,"XY"); 
  gStyle->SetTitleFont(42,"XY");
  gStyle->SetEndErrorSize(0);
}

void LoadParameters(TString datafile,
		    std::vector<float> &v_M1,
		    std::vector<float> &v_M3,	
		    std::vector<float> &v_mu,	
		    std::vector<float> &v_BRgam,	
		    std::vector<float> &v_BRz,
		    std::vector<float> &v_BRh,
		    std::vector<float> &v_chi10_mass,
		    std::vector<float> &v_chi10_width,
		    std::vector<float> &v_chi10_lenght,
		    std::vector<float> &v_gl_width,
		    std::vector<float> &v_gl_lenght,
		    std::vector<float> &v_BRdirect,
		    std::vector<float> &v_hM,
		    TString musign){

  string M1,M3,mu,Msq,chi10_mass,BRtoGgam,BRtoGZ,BRtoGh,chi10Width,chi10Lenght,chi20_mass,chi20Width,chi20Lenght,chi20BRtoGgam,chi20BRtoGz,chi20BRtoGh,chi20BRdom_str,chi20BRdom,glWidth,glLenght,BRsgtochi10,BRsgtochi20,BRsgtoG,Hmass,Gmass;
  string line;
  ifstream infile(datafile);
  while (true){
    getline(infile, line); 
    if (line[0]=="#") continue; //avoid commented header
    infile >> M1 >> M3 >> mu >> Msq >> chi10_mass >> BRtoGgam >> BRtoGZ >> BRtoGh >> chi10Width >> chi10Lenght >> chi20_mass >> chi20Width >> chi20Lenght >> chi20BRtoGgam >> chi20BRtoGz >> chi20BRtoGh >> chi20BRdom_str >> chi20BRdom >> glWidth >> glLenght >> BRsgtochi10 >> BRsgtochi20 >> BRsgtoG >> Hmass >> Gmass;

    if( infile.eof() ) break; //to avoid reading the last line twice

    //decide what to do according to mu value
    float vmu = atof( mu.c_str() );
    if(musign=="plus" && vmu < 0) continue;
    if(musign=="minus" && vmu > 0) continue;
    if(musign=="fabs") vmu = fabs(vmu);

    v_M1.push_back(atof( M1.c_str() ));
    v_M3.push_back(atof( M3.c_str() ));
    v_mu.push_back( vmu );
    v_BRgam.push_back(atof( BRtoGgam.c_str() ));	
    v_BRz.push_back(atof( BRtoGZ.c_str() ));
    v_BRh.push_back(atof( BRtoGh.c_str() ));
    v_chi10_mass.push_back(atof( chi10_mass.c_str() ));
    v_chi10_width.push_back(atof( chi10Width.c_str() ));
    v_chi10_lenght.push_back(atof( chi10Lenght.c_str() )*1000.); //in mm
    v_gl_width.push_back(atof( glWidth.c_str() ));
    v_gl_lenght.push_back(atof(glLenght.c_str() )*1000.); //in mm
    v_BRdirect.push_back(atof( BRsgtoG.c_str() ));
    v_hM.push_back(atof( Hmass.c_str() ));
  }

}

int FillHistogram(TH2F* hV, TH2F* hN, int binx, int biny, float value, bool Kfactor=1., bool checkPositive=true, bool debug=false){

  float cv = hV->GetBinContent(binx, biny)*Kfactor;
  float cn = hN->GetBinContent(binx, biny);
  
  if(checkPositive && value<0) return 0;  

  float cv = ( (cv*cn) + value ) / (cn+1);
  cn++;

  if(debug) cout << "cv = " << cv << endl;

  hV->SetBinContent(binx, biny, cv);
  hN->SetBinContent(binx, biny, cn);
  return 0;
}

void MakePlots(TString datafile="output/SinglePhotonGrid_out_pars.dat", TString musign="", TString opath="output/"){ //musign="all","plus","minus","fabs"

  SetStyle();

  std::vector<float> v_M1;
  std::vector<float> v_M3;
  std::vector<float> v_mu;
  std::vector<float> v_BRgam;
  std::vector<float> v_BRz;
  std::vector<float> v_BRh;
  std::vector<float> v_chi10_mass;
  std::vector<float> v_chi10_width;
  std::vector<float> v_chi10_lenght;
  std::vector<float> v_gl_width;
  std::vector<float> v_gl_lenght;
  std::vector<float> v_BRdirect;
  std::vector<float> v_hM;

  LoadParameters(datafile,
		 v_M1,
		 v_M3,	
		 v_mu,	
		 v_BRgam,	
		 v_BRz,
		 v_BRh,
		 v_chi10_mass,
		 v_chi10_width,
		 v_chi10_lenght,
		 v_gl_width,
		 v_gl_lenght,
		 v_BRdirect,
		 v_hM,
		 musign);

  //mu "all" by default  
  float mu_min = -1300;
  float mu_max =  1300;
  int   mu_bins = 100;
  float m1mu_min = -3;
  float m1mu_max =  3;
  int   m1mu_bins = 120;
  TString mulabel="#mu [GeV]";
  TString m1mulabel="M1/#mu"; 

  if(musign=="plus"){
    mu_min =  500;
    mu_max =  1300;
    mu_bins = 50;
    m1mu_min =  0;
    m1mu_max =  3;
    m1mu_bins = 60;
    mulabel="#mu [GeV]";
    m1mulabel="M1/#mu"; 
    opath+="/mu_plus/";
  }
  else if(musign=="minus"){
    mu_min =  -1300;
    mu_max =  -500;
    mu_bins = 50;
    m1mu_min =  -3;
    m1mu_max =  0;
    m1mu_bins = 60;
    mulabel="#mu [GeV]";
    m1mulabel="M1/#mu"; 
    opath+="/mu_minus/";
  }
  else if(musign=="fabs"){
    mu_min =  500;
    mu_max =  1300;
    mu_bins = 50;
    m1mu_min =  0;
    m1mu_max =  3;
    m1mu_bins = 60;
    mulabel="|#mu| [GeV]";
    m1mulabel="M1/|#mu|"; 
    opath+="/mu_fabs/";
  }
  else{
    opath +="/mu_all/";
  }
  //define histograms
  //VALUES
  //chi10 mass
  TH1F* h_chi10M = new TH1F("h_chi10M","#chi_0 mass [GeV]",100,400,1400);
  TH2F* h_M1_mu_chi10M = new TH2F("h_M1_mu_chi10M","#chi_0 mass [GeV];M1 [GeV];"+mulabel,50,500,1300,mu_bins,mu_min,mu_max);
  TH2F* h_M1mu_M3_chi10M = new TH2F("h_M1mu_M3_chi10M","#chi_0 mass [GeV];"+m1mulabel+";M3 [GeV]",m1mu_bins,m1mu_min,m1mu_max,10,800,1300);

  //BRs
  TH2F* h_M1_mu_BRgam = new TH2F("h_M1_mu_BRgam","BR(chi10->~G+gam);M1;|#mu| [GeV]",50,500,1300,mu_bins,mu_min,mu_max);
  TH2F* h_M1_mu_BRz   = new TH2F("h_M1_mu_BRz","BR(chi10->~G+Z);M1;|#mu| [GeV]",50,500,1300,mu_bins,mu_min,mu_max);
  TH2F* h_M1_mu_BRh   = new TH2F("h_M1_mu_BRh","BR(chi10->~G+H);M1;|#mu| [GeV]",50,500,1300,mu_bins,mu_min,mu_max);

  TH2F* h_M1mu_M3_BRgam = new TH2F("h_M1mu_M3_BRgam","BR(chi10->~G+gam);"+m1mulabel+";M3 [GeV]",m1mu_bins,m1mu_min,m1mu_max,10,800,1300);
  TH2F* h_M1mu_M3_BRz   = new TH2F("h_M1mu_M3_BRz","BR(chi10->~G+Z);"+m1mulabel+";M3 [GeV]",m1mu_bins,m1mu_min,m1mu_max,10,800,1300);
  TH2F* h_M1mu_M3_BRh   = new TH2F("h_M1mu_M3_BRh","BR(chi10->~G+H);"+m1mulabel+";M3 [GeV]",m1mu_bins,m1mu_min,m1mu_max,10,800,1300);

  TH2F* h_chi10M_M3_BRgam = new TH2F("h_chi10M_M3_BRgam","BR(chi10->~G+gam);M(#chi_0) [GeV];M3 [GeV]",50,500,1000,10,800,1300);
  TH2F* h_chi10M_M3_BRz   = new TH2F("h_chi10M_M3_BRz","BR(chi10->~G+Z);M(#chi_0) [GeV];M3 [GeV]",50,500,1000,10,800,1300);
  TH2F* h_chi10M_M3_BRh   = new TH2F("h_chi10M_M3_BRh","BR(chi10->~G+H);M(#chi_0) [GeV];M3 [GeV]",50,500,1000,10,800,1300);

  //Decay Lenghts
  TH2F* h_M1_mu_chi10L = new TH2F("h_M1_mu_chi10L","#chi_0 decay lenght [mm];M1 [GeV];"+mulabel,50,500,1300,mu_bins,mu_min,mu_max);
  TH2F* h_M1_mu_glL    = new TH2F("h_M1_mu_glL","gluino decay lenght [mm];M1 [GeV];"+mulabel,50,500,1300,mu_bins,mu_min,mu_max);

  TH2F* h_M1mu_M3_chi10L = new TH2F("h_M1mu_M3_chi10L","#chi_0 decay lenght [mm];"+m1mulabel+";M3 [GeV]",m1mu_bins,m1mu_min,m1mu_max,10,800,1300);
  TH2F* h_M1mu_M3_glL    = new TH2F("h_M1mu_M3_glL   ","gluino decay lenght [mm];"+m1mulabel+";M3 [GeV]",m1mu_bins,m1mu_min,m1mu_max,10,800,1300);

  TH2F* h_chi10M_M3_chi10L = new TH2F("h_chi10M_M3_chi10L","#chi_0 decay lenght [mm];M(#chi_0) [GeV];M3 [GeV]",50,500,1000,10,800,1300);
  TH2F* h_chi10M_M3_glL    = new TH2F("h_chi10M_M3_glL   ","gluino decay lenght [mm];M(#chi_0) [GeV];M3 [GeV]",50,500,1000,10,800,1300);

  //Direct gluino decay 
  TH2F* h_M1_mu_BRgltochi10 = new TH2F("h_M1_mu_BRgltochi10","BR(gl->g+~G);M1 [GeV];"+mulabel+"",50,500,1300,mu_bins,mu_min,mu_max);
  TH2F* h_M1mu_M3_BRgltochi10 = new TH2F("h_M1mu_M3_BRgltochi10","BR(gl->g+~G);"+m1mulabel+";M3 [GeV]",m1mu_bins,m1mu_min,m1mu_max,10,800,1300);
  TH2F* h_chi10M_M3_BRgltochi10 = new TH2F("h_chi10M_M3_BRgltochi10","BR(gl->g+~G);M(#chi_0) [GeV];M3 [GeV]",50,500,1000,10,800,1300);

  //Higgs Mass
  TH1F* h_hM = new TH1F("h_hM","light Higgs mass [GeV]",100,50,150);
  TH2F* h_M1_mu_hM = new TH2F("h_M1_mu_hM","light Higgs mass [GeV];M1 [GeV];"+mulabel+"",50,500,1300,mu_bins,mu_min,mu_max);
  TH2F* h_M1mu_M3_hM = new TH2F("h_M1mu_M3_hM","light Higgs mass [GeV];"+m1mulabel+";M3 [GeV]",m1mu_bins,m1mu_min,m1mu_max,10,800,1300);
  TH2F* h_chi10M_M3_hM = new TH2F("h_chi10M_M3_hM","light Higgs mass [GeV];M(#chi_0) [GeV];M3 [GeV]",50,500,1000,10,800,1300);
  
  //FILL ATTEMPTS
  //chi10 mass
  TH2F* Nh_M1_mu_chi10M = (TH2F*) h_M1_mu_chi10M->Clone();  Nh_M1_mu_chi10M->SetName("Nh_M1_mu_chi10M");
  TH2F* Nh_M1mu_M3_chi10M = (TH2F*) h_M1mu_M3_chi10M->Clone(); Nh_M1mu_M3_chi10M->SetName("Nh_M1mu_M3_chi10M"); 

  //BRs
  TH2F* Nh_M1_mu_BRgam = (TH2F*) h_M1_mu_BRgam->Clone(); Nh_M1_mu_BRgam->SetName("Nh_M1_mu_BRgam"); 
  TH2F* Nh_M1_mu_BRz   = (TH2F*) h_M1_mu_BRz->Clone(); Nh_M1_mu_BRz->SetName("Nh_M1_mu_BRz");
  TH2F* Nh_M1_mu_BRh   = (TH2F*) h_M1_mu_BRh->Clone(); Nh_M1_mu_BRh->SetName("Nh_M1_mu_BRh");

  TH2F* Nh_M1mu_M3_BRgam = (TH2F*) h_M1mu_M3_BRgam->Clone(); Nh_M1mu_M3_BRgam->SetName("Nh_M1mu_M3_BRgam");
  TH2F* Nh_M1mu_M3_BRz   = (TH2F*) h_M1mu_M3_BRgam->Clone(); Nh_M1mu_M3_BRz->SetName("Nh_M1mu_M3_BRz");
  TH2F* Nh_M1mu_M3_BRh   = (TH2F*) h_M1mu_M3_BRgam->Clone(); Nh_M1mu_M3_BRh->SetName("Nh_M1mu_M3_BRh");

  TH2F* Nh_chi10M_M3_BRgam = (TH2F*) h_chi10M_M3_BRgam->Clone(); Nh_chi10M_M3_BRgam->SetName("Nh_chi10M_M3_BRgam");
  TH2F* Nh_chi10M_M3_BRz   = (TH2F*) h_chi10M_M3_BRgam->Clone(); Nh_chi10M_M3_BRz->SetName("Nh_chi10M_M3_BRz");
  TH2F* Nh_chi10M_M3_BRh   = (TH2F*) h_chi10M_M3_BRgam->Clone(); Nh_chi10M_M3_BRh->SetName("Nh_chi10M_M3_BRh");

  //Decay Lenghts
  TH2F* Nh_M1_mu_chi10L = (TH2F*) h_M1_mu_chi10L->Clone(); Nh_M1_mu_chi10L->SetName("Nh_M1_mu_chi10L");
  TH2F* Nh_M1_mu_glL    = (TH2F*) h_M1_mu_glL->Clone(); Nh_M1_mu_glL->SetName("Nh_M1_mu_glL");

  TH2F* Nh_M1mu_M3_chi10L = (TH2F*) h_M1mu_M3_chi10L->Clone(); Nh_M1mu_M3_chi10L->SetName("Nh_M1mu_M3_chi10L");
  TH2F* Nh_M1mu_M3_glL    = (TH2F*) h_M1mu_M3_glL->Clone(); Nh_M1mu_M3_glL->SetName("Nh_M1mu_M3_glL");

  TH2F* Nh_chi10M_M3_chi10L = (TH2F*) h_chi10M_M3_chi10L->Clone(); Nh_chi10M_M3_chi10L->SetName("Nh_chi10M_M3_chi10L");
  TH2F* Nh_chi10M_M3_glL    = (TH2F*) h_chi10M_M3_glL->Clone(); Nh_chi10M_M3_glL->SetName("Nh_chi10M_M3_glL");

  //Direct gluino decay 
  TH2F* Nh_M1_mu_BRgltochi10 = (TH2F*) h_M1_mu_BRgltochi10->Clone(); Nh_M1_mu_BRgltochi10->SetName("Nh_M1_mu_BRgltochi10");
  TH2F* Nh_M1mu_M3_BRgltochi10 = (TH2F*) h_M1mu_M3_BRgltochi10->Clone(); Nh_M1mu_M3_BRgltochi10->SetName("Nh_M1mu_M3_BRgltochi10");
  TH2F* Nh_chi10M_M3_BRgltochi10 = (TH2F*) h_chi10M_M3_BRgltochi10->Clone(); Nh_chi10M_M3_BRgltochi10->SetName("Nh_chi10M_M3_BRgltochi10");

  //Higgs mass
  TH2F* Nh_M1_mu_hM = (TH2F*) h_M1_mu_hM->Clone(); Nh_M1_mu_hM->SetName("Nh_M1_mu_hM");
  TH2F* Nh_M1mu_M3_hM = (TH2F*) h_M1mu_M3_hM->Clone(); Nh_M1mu_M3_hM->SetName("Nh_M1mu_M3_hM");
  TH2F* Nh_chi10M_M3_hM = (TH2F*) h_chi10M_M3_hM->Clone(); Nh_chi10M_M3_hM->SetName("Nh_chi10M_M3_hM");


  //Fill histograms
  for(unsigned int i=0; i<v_mu.size();i++){

    int b_M1 = h_M1_mu_chi10M->GetXaxis()->FindBin(v_M1[i]);
    int b_mu = fabs(h_M1_mu_chi10M->GetYaxis()->FindBin(v_mu[i]));
    int b_M1mu = h_M1mu_M3_chi10M->GetXaxis()->FindBin(v_M1[i]/v_mu[i]);
    int b_M3 = h_M1mu_M3_chi10M->GetYaxis()->FindBin(v_M3[i]);
    int b_chi10M = h_chi10M_M3_BRgam->GetXaxis()->FindBin(v_chi10_mass[i]);

    h_chi10M->Fill(v_chi10_mass[i]);

    FillHistogram(h_M1_mu_chi10M, Nh_M1_mu_chi10M, b_M1, b_mu, v_chi10_mass[i]);
    FillHistogram(h_M1mu_M3_chi10M, Nh_M1mu_M3_chi10M, b_M1mu, b_M3, v_chi10_mass[i]);

    FillHistogram(h_M1_mu_BRgam, Nh_M1_mu_BRgam, b_M1, b_mu, v_BRgam[i]);
    FillHistogram(h_M1_mu_BRz, Nh_M1_mu_BRz, b_M1, b_mu, v_BRz[i]);
    FillHistogram(h_M1_mu_BRh, Nh_M1_mu_BRh, b_M1, b_mu, v_BRh[i]);

    FillHistogram(h_M1mu_M3_BRgam, Nh_M1mu_M3_BRgam, b_M1mu, b_M3, v_BRgam[i]);
    FillHistogram(h_M1mu_M3_BRz, Nh_M1mu_M3_BRz, b_M1mu, b_M3, v_BRz[i]);
    FillHistogram(h_M1mu_M3_BRh, Nh_M1mu_M3_BRh, b_M1mu, b_M3, v_BRh[i]);

    FillHistogram(h_chi10M_M3_BRgam, Nh_chi10M_M3_BRgam, b_chi10M, b_M3, v_BRgam[i]);
    FillHistogram(h_chi10M_M3_BRz, Nh_chi10M_M3_BRz, b_chi10M, b_M3, v_BRz[i]);
    FillHistogram(h_chi10M_M3_BRh, Nh_chi10M_M3_BRh, b_chi10M, b_M3, v_BRh[i]);

    FillHistogram(h_M1_mu_chi10L, Nh_M1_mu_chi10L, b_M1, b_mu, v_chi10_lenght[i]); //in mm
    FillHistogram(h_M1mu_M3_chi10L, Nh_M1mu_M3_chi10L, b_M1mu, b_M3, v_chi10_lenght[i]); //in mm
    FillHistogram(h_chi10M_M3_chi10L, Nh_chi10M_M3_chi10L, b_chi10M, b_M3, v_chi10_lenght[i]); //in mm
			      
    FillHistogram(h_M1_mu_glL, Nh_M1_mu_glL, b_M1, b_mu, v_gl_lenght[i]); //in mm 
    FillHistogram(h_M1mu_M3_glL, Nh_M1mu_M3_glL, b_M1mu, b_M3, v_gl_lenght[i]); //in mm
    FillHistogram(h_chi10M_M3_glL, Nh_chi10M_M3_glL, b_chi10M, b_M3, v_gl_lenght[i]); //in mm

    FillHistogram(h_M1_mu_BRgltochi10, Nh_M1_mu_BRgltochi10, b_M1, b_mu, v_BRdirect[i]);
    FillHistogram(h_M1mu_M3_BRgltochi10, Nh_M1mu_M3_BRgltochi10, b_M1mu, b_M3, v_BRdirect[i]);
    FillHistogram(h_chi10M_M3_BRgltochi10, Nh_chi10M_M3_BRgltochi10, b_chi10M, b_M3, v_BRdirect[i]);

    h_hM->Fill(v_hM[i]);
    FillHistogram(h_M1_mu_hM, Nh_M1_mu_hM, b_M1, b_mu, v_hM[i]);
    FillHistogram(h_M1mu_M3_hM, Nh_M1mu_M3_hM, b_M1mu, b_M3, v_hM[i]);
    FillHistogram(h_chi10M_M3_hM, Nh_chi10M_M3_hM, b_chi10M, b_M3, v_hM[i]);
  }

  //Set Style
  h_chi10M->GetYaxis()->SetTitleOffset(1.3);
  h_M1_mu_chi10M->GetYaxis()->SetTitleOffset(1.3);
  h_M1mu_M3_chi10M->GetYaxis()->SetTitleOffset(1.3);
  h_M1_mu_BRgam->GetYaxis()->SetTitleOffset(1.3);
  h_M1_mu_BRz->GetYaxis()->SetTitleOffset(1.3);
  h_M1_mu_BRh->GetYaxis()->SetTitleOffset(1.3);
  h_M1mu_M3_BRgam->GetYaxis()->SetTitleOffset(1.3);
  h_M1mu_M3_BRz->GetYaxis()->SetTitleOffset(1.3);
  h_M1mu_M3_BRh->GetYaxis()->SetTitleOffset(1.3);
  h_chi10M_M3_BRgam->GetYaxis()->SetTitleOffset(1.3);
  h_chi10M_M3_BRz->GetYaxis()->SetTitleOffset(1.3);
  h_chi10M_M3_BRh->GetYaxis()->SetTitleOffset(1.3);
  h_M1_mu_chi10L->GetYaxis()->SetTitleOffset(1.3);
  h_M1mu_M3_chi10L->GetYaxis()->SetTitleOffset(1.3);
  h_chi10M_M3_chi10L->GetYaxis()->SetTitleOffset(1.3);
  h_M1_mu_glL->GetYaxis()->SetTitleOffset(1.3);
  h_M1mu_M3_glL->GetYaxis()->SetTitleOffset(1.3);
  h_chi10M_M3_glL->GetYaxis()->SetTitleOffset(1.3);
  h_M1_mu_BRgltochi10->GetYaxis()->SetTitleOffset(1.3);
  h_M1mu_M3_BRgltochi10->GetYaxis()->SetTitleOffset(1.3);
  h_chi10M_M3_BRgltochi10->GetYaxis()->SetTitleOffset(1.3);
  h_hM->GetYaxis()->SetTitleOffset(1.3);
  h_M1_mu_hM->GetYaxis()->SetTitleOffset(1.3);
  h_M1mu_M3_hM->GetYaxis()->SetTitleOffset(1.3);
  h_chi10M_M3_hM->GetYaxis()->SetTitleOffset(1.3);

  //Draw histograms
  TCanvas* c0 =  new TCanvas("c0");
  c0->cd(); c0->SetLeftMargin(0.12);// c0->SetRightMargin(0.15);
  h_chi10M->Draw("hist");
  c0->SaveAs(opath+"h_chi10M.png");

  TCanvas* c1 =  new TCanvas("c1");
  c1->cd(); c1->SetLeftMargin(0.12); c1->SetRightMargin(0.15);
  h_M1_mu_chi10M->Draw("colz");
  c1->SaveAs(opath+"h_M1_mu_chi10M.png");

  TCanvas* c2 =  new TCanvas("c2");
  c2->cd(); c2->SetLeftMargin(0.12); c2->SetRightMargin(0.15);
  h_M1mu_M3_chi10M->Draw("colz");
  c2->SaveAs(opath+"h_M1mu_M3_chi10M.png");

  TCanvas* c3 =  new TCanvas("c3");
  c3->cd(); c3->SetLeftMargin(0.12); c3->SetRightMargin(0.15);
  h_M1_mu_BRgam->Draw("colz");
  c3->SaveAs(opath+"h_M1_mu_BRgam.png");

  TCanvas* c4 =  new TCanvas("c4");
  c4->cd(); c4->SetLeftMargin(0.12); c4->SetRightMargin(0.15);
  h_M1_mu_BRz->Draw("colz");
  c4->SaveAs(opath+"h_M1_mu_BRz.png");

  TCanvas* c5 =  new TCanvas("c5");
  c5->cd(); c5->SetLeftMargin(0.12); c5->SetRightMargin(0.15);
  h_M1_mu_BRh->Draw("colz");
  c5->SaveAs(opath+"h_M1_mu_BRh.png");

  TCanvas* c6 =  new TCanvas("c6");
  c6->cd(); c6->SetLeftMargin(0.12); c6->SetRightMargin(0.15);
  h_M1mu_M3_BRgam->Draw("colz");
  c6->SaveAs(opath+"h_M1mu_M3_BRgam.png");

  TCanvas* c7 =  new TCanvas("c7");
  c7->cd(); c7->SetLeftMargin(0.12); c7->SetRightMargin(0.15);
  h_M1mu_M3_BRz->Draw("colz");
  c7->SaveAs(opath+"h_M1mu_M3_BRz.png");

  TCanvas* c8 =  new TCanvas("c8");
  c8->cd(); c8->SetLeftMargin(0.12); c8->SetRightMargin(0.15);
  h_M1mu_M3_BRh->Draw("colz");
  c8->SaveAs(opath+"h_M1mu_M3_BRh.png");

  TCanvas* c6b =  new TCanvas("c6b");
  c6b->cd(); c6b->SetLeftMargin(0.12); c6b->SetRightMargin(0.15);
  h_chi10M_M3_BRgam->Draw("colz");
  c6b->SaveAs(opath+"h_chi10M_M3_BRgam.png");

  TCanvas* c7b =  new TCanvas("c7b");
  c7b->cd(); c7b->SetLeftMargin(0.12); c7b->SetRightMargin(0.15);
  h_chi10M_M3_BRz->Draw("colz");
  c7b->SaveAs(opath+"h_chi10M_M3_BRz.png");

  TCanvas* c8b =  new TCanvas("c8b");
  c8b->cd(); c8b->SetLeftMargin(0.12); c8b->SetRightMargin(0.15);
  h_chi10M_M3_BRh->Draw("colz");
  c8b->SaveAs(opath+"h_chi10M_M3_BRh.png");

  TCanvas* c9 =  new TCanvas("c9");
  c9->cd(); c9->SetLeftMargin(0.12); c9->SetRightMargin(0.15);
  h_M1_mu_chi10L->Draw("colz");
  c9->SaveAs(opath+"h_M1_mu_chi10L.png");

  TCanvas* c10 =  new TCanvas("c10");
  c10->cd(); c10->SetLeftMargin(0.12); c10->SetRightMargin(0.15);
  h_M1mu_M3_chi10L->Draw("colz");
  c10->SaveAs(opath+"h_M1mu_M3_chi10L.png");

  TCanvas* c10b =  new TCanvas("c10b");
  c10b->cd(); c10b->SetLeftMargin(0.12); c10b->SetRightMargin(0.15);
  h_chi10M_M3_chi10L->Draw("colz");
  c10b->SaveAs(opath+"h_chi10M_M3_chi10L.png");

  TCanvas* c11 =  new TCanvas("c11");
  c11->cd(); c11->SetLeftMargin(0.12); c11->SetRightMargin(0.15);
  h_M1_mu_glL->Draw("colz");
  c11->SaveAs(opath+"h_M1_mu_glL.png");

  TCanvas* c12 =  new TCanvas("c12");
  c12->cd(); c12->SetLeftMargin(0.12); c12->SetRightMargin(0.15);
  h_M1mu_M3_glL->Draw("colz");
  c12->SaveAs(opath+"h_M1mu_M3_glL.png");

  TCanvas* c12b =  new TCanvas("c12b");
  c12b->cd(); c12b->SetLeftMargin(0.12); c12b->SetRightMargin(0.15);
  h_chi10M_M3_glL->Draw("colz");
  c12b->SaveAs(opath+"h_chi10M_M3_glL.png");

  TCanvas* c13 =  new TCanvas("c13");
  c13->cd(); c13->SetLeftMargin(0.12); c13->SetRightMargin(0.15);
  h_M1_mu_BRgltochi10->Draw("colz");
  c13->SaveAs(opath+"h_M1_mu_BRgltochi10.png");

  TCanvas* c13b =  new TCanvas("c13b");
  c13b->cd(); c13b->SetLeftMargin(0.12); c13b->SetRightMargin(0.15);
  h_M1mu_M3_BRgltochi10->Draw("colz");
  c13b->SaveAs(opath+"h_M1mu_M3_BRgltochi10.png");

  TCanvas* c14b =  new TCanvas("c14b");
  c14b->cd(); c14b->SetLeftMargin(0.12); c14b->SetRightMargin(0.15);
  h_chi10M_M3_BRgltochi10->Draw("colz");
  c14b->SaveAs(opath+"h_chi10M_M3_BRgltochi10.png");

  TCanvas* c15 =  new TCanvas("c15");
  c15->cd(); c15->SetLeftMargin(0.12); c15->SetRightMargin(0.15);
  h_hM->Draw("hist");
  c15->SaveAs(opath+"h_hM.png");

  TCanvas* c16 =  new TCanvas("c16");
  c16->cd(); c16->SetLeftMargin(0.12); c16->SetRightMargin(0.15);
  h_M1_mu_hM->Draw("colz");
  c16->SaveAs(opath+"h_M1_mu_hM.png");

  TCanvas* c17 =  new TCanvas("c17");
  c17->cd(); c17->SetLeftMargin(0.12); c17->SetRightMargin(0.15);
  h_M1mu_M3_hM->Draw("colz");
  c17->SaveAs(opath+"h_M1mu_M3_hM.png");

  TCanvas* c18 =  new TCanvas("c18");
  c18->cd(); c18->SetLeftMargin(0.12); c18->SetRightMargin(0.15);
  h_chi10M_M3_hM->Draw("colz");
  c18->SaveAs(opath+"h_chi10M_M3_hM.png");

}
