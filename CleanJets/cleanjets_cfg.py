import FWCore.ParameterSet.Config as cms

process = cms.Process("CLEANJETS")

#######################################
# Loading all processes and functions
#######################################
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.Geometry.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load('TrackingTools.TransientTrack.TransientTrackBuilder_cfi')
process.GlobalTag.globaltag = cms.string('80X_mcRun2_asymptotic_v14')
process.load("Tools.CleanJets.cleanjets_cfi")

#######################################
# Declaring Input and configurations
#######################################
process.source = cms.Source("PoolSource",
#        fileNames = cms.untracked.vstring('root://eoscms//eos/cms/store/user/ktos/heavyHiggs_125_light_9_2mu2tau_RECO2/heavyHiggs_125_light_9_2mu2tau_RECO2_NUM.root')
#       fileNames = cms.untracked.vstring('root://eoscms//eos/cms/store/user/ktos/heavyHiggs_125_light_9_2mu2tau_RECO2/heavyHiggs_125_light_9_2mu2tau_RECO2_NUM.root')
       fileNames = cms.untracked.vstring('root://eoscms//eos/cms/store/group/phys_higgs/HiggsExo/ktos/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/CRAB3_WJ_CJ_Lumi200000_Trig_NewMVA_SEP14/160914_200806/0000/DYHighMass_data_no_selection_NUM.root')
#       fileNames = cms.untracked.vstring('root://eoscms//eos/cms/store/group/phys_higgs/HiggsExo/ktos/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/CRAB3_WJ_CJ_Lumi200000_Trig_New_SEP14/160914_200909/0000/DYHighMass_data_no_selection_NUM.root')
#       fileNames = cms.untracked.vstring('root://eoscms//eos/cms/store/group/phys_higgs/HiggsExo/ktos/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/CRAB3_WJ_CJ_Lumi200000_Trig_Old_SEP14/160914_200957/0000/DYHighMass_data_no_selection_NUM.root')
#        fileNames = cms.untracked.vstring('root://eoscms//eos/cms/store/group/phys_higgs/HiggsExo/ktos/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/CRAB3_WJ_CJ_Lumi200000_Trig_OldMVA_SEP14/160914_201040/0000/DYHighMass_data_no_selection_NUM.root')


)


process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )


process.CleanJets.outFileName = cms.string('/afs/cern.ch/user/k/ktos/GroupDir/CMSSW_8_0_17/src/Tools/CleanJets/BSUB/DIRNAME/CleanJets_Plots_NUM.root')

#######################################
# HPS Tau Reconstruction alterations 
#######################################
process.load("RecoTauTag.Configuration.RecoPFTauTag_cff")
process.ak4PFJetTracksAssociatorAtVertex.jets = cms.InputTag('CleanJets', 'ak4PFJetsNoMu', 'CLEANJETS')
process.recoTauAK4PFJets08Region.src = cms.InputTag('CleanJets', 'ak4PFJetsNoMu', 'CLEANJETS')

process.ak4PFJetsLegacyHPSPiZeros.jetSrc = cms.InputTag('CleanJets', 'ak4PFJetsNoMu', 'CLEANJETS')
process.ak4PFJetsRecoTauChargedHadrons.jetSrc = cms.InputTag('CleanJets', 'ak4PFJetsNoMu', 'CLEANJETS')
process.combinatoricRecoTaus.jetSrc = cms.InputTag('CleanJets', 'ak4PFJetsNoMu', 'CLEANJETS')

#########################################
# Rerunning bTaggin on CleanJets Sample
#########################################
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.Geometry.GeometryRecoDB_cff")  #Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff") #Configuration.StandardSequences.FrontierConditions_CMS.GlobalTag_cff")

from RecoBTag.Configuration.RecoBTag_cff import *
from RecoBTag.SoftLepton.softLepton_cff import *
from RecoBTag.ImpactParameter.impactParameter_cff import *
from RecoBTag.SecondaryVertex.secondaryVertex_cff import *
from RecoBTag.Combined.combinedMVA_cff import *
from RecoBTag.CTagging.RecoCTagging_cff import *
from RecoVertex.AdaptiveVertexFinder.inclusiveVertexing_cff import *
process.pfImpactParameterTagInfos.jets = cms.InputTag('CleanJets', 'ak4PFJetsNoMu', 'CLEANJETS')
process.softPFMuonsTagInfos.jets = cms.InputTag('CleanJets', 'ak4PFJetsNoMu', 'CLEANJETS')
process.softPFElectronsTagInfos.jets = cms.InputTag('CleanJets', 'ak4PFJetsNoMu', 'CLEANJETS')

process.pfBTagging = cms.Sequence(
    (
      # impact parameters and IP-only algorithms
      pfImpactParameterTagInfos *
      ( pfTrackCountingHighEffBJetTags +
        pfJetProbabilityBJetTags +
        pfJetBProbabilityBJetTags +

        # SV tag infos depending on IP tag infos, and SV (+IP) based algos
        pfSecondaryVertexTagInfos *
        ( pfSimpleSecondaryVertexHighEffBJetTags +
          pfCombinedSecondaryVertexV2BJetTags
        )
        + inclusiveCandidateVertexing *
        pfInclusiveSecondaryVertexFinderTagInfos *
        pfSimpleInclusiveSecondaryVertexHighEffBJetTags *
        pfCombinedInclusiveSecondaryVertexV2BJetTags

      ) +

      # soft lepton tag infos and algos
      softPFMuonsTagInfos *
      softPFMuonBJetTags
      + softPFElectronsTagInfos *
      softPFElectronBJetTags
    ) *

    # overall combined taggers
    ( #CSV + soft-lepton + jet probability discriminators combined
      pfCombinedMVAV2BJetTags

    )
)

#######################################
# Configuring Output
#######################################
process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('file:DIRNAME_NUM.root'),
    SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('p')),
)

process.p = cms.Path(process.muonsRef*
                     process.CleanJets*
                     process.PFTau*
                     process.pfBTagging)
process.e = cms.EndPath(process.out)

