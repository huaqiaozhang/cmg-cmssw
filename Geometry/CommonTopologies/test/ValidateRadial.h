#ifndef VALIDATE_RADIAL_H
#define VALIDATE_RADIAL_H

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "Geometry/CommonTopologies/interface/RadialStripTopology.h"
#include <vector>
#include <iostream>
#include "TFile.h"

class ValidateRadial : public edm::EDAnalyzer {
 public:
  ValidateRadial(const edm::ParameterSet&);
 private:
  void analyze(const edm::Event& e, const edm::EventSetup& es);
  std::vector<const RadialStripTopology*> get_list_of_radial_topologies(const edm::Event&, const edm::EventSetup&);
  void test_topology(const RadialStripTopology* , unsigned);
  bool pass_frame_change_test(const RadialStripTopology* t, const float strip, const float stripErr2, const bool);
  bool EQUAL(const double a, const double b) {return fabs(a-b)<epsilon_;}
  const double epsilon_;
  TFile* file_;
  const bool printOut_;
};

#endif
