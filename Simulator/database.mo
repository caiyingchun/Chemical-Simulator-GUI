package database
model Water extends Simulator.Files.Chemsep_Database.General_Properties(name = "Water", CAS = "7732-18-5", Tc = 647.14, Pc = 2.2064E+07,  Vc = 0.05595, Cc = 0.229, Tb = 373.15, Tm = 273.15, TT = 273.16, TP = 611.73, MW = 18.015, LVB = 0.01807, AF = 0.344, SP = 47860, DM = 6.17E-30, IGHF = -2.41814E+08, GEF = -2.2859E+08, AS = 188724, HFMP = 6001740, HOC = 0, LiqDen = {106,32.51621,-3.213004,7.92411,-7.359898,2.703522}, VP = {101,74.55502,-7295.586,-7.442448,0.0000042881,2}, LiqCp = {16,75539,-22297,136.02,-0.25622,0.00018273}, HOV = {106,5.964E+07,0.86515,-1.1134,0.67764,-0.026925}, VapCp = {16,33200,-878.9001,8.436956,0.00207627,-6.467085E-07}, LiqVis = {101,-133.7,6785.7,18.47,-0.000014736,2}, VapVis = {102,7.002327E-08,0.934576,195.6338,-13045.99,0}, LiqK = {16,-1.5697,-55.141,0.7832,0.0011484,-0.0000018151}, VapK = {102,0.0000065986,1.3947,59.478,-15484,0}, Racketparam = 0.2338, UniquacR = 0.92, UniquacQ = 1.4, ChaoSeadAF = 0.328, ChaoSeadSP = 47812.7, ChaoSeadLV = 0.0180674);
end Water;model Oxygen extends Simulator.Files.Chemsep_Database.General_Properties(name = "Oxygen", CAS = "7782-44-7", Tc = 154.58, Pc = 5043000,  Vc = 0.07337, Cc = 0.288, Tb = 90.17, Tm = 54.361, TT = 54.361, TP = 150, MW = 31.999, LVB = 0.02785, AF = 0.022, SP = 8182, DM = 0, IGHF = 0, GEF = 0, AS = 205043, HFMP = 444000, HOC = 0, LiqDen = {105,2.6097,0.23614,154.78,0.23695,0}, VP = {101,40.55487,-1120.543,-3.776114,0.0000485344,2}, LiqCp = {16,53393,-1966.4,48.21,-0.31631,0.0010466}, HOV = {106,1.0672E+07,1.5661,-3.4356,3.5416,-1.2718}, VapCp = {16,29061.62,-1470.897,11.10778,-0.00128484,3.183122E-07}, LiqVis = {101,-5.2319,116.13,-1.0315,0.0000034376,2}, VapVis = {102,8.0134E-07,0.60321,56.09,1584.9,0}, LiqK = {16,-0.19654,-10.535,-0.46717,-0.0052064,-3.3418E-07}, VapK = {102,0.0004508,0.74544,58.278,-562.62,0}, Racketparam = 0.2908, UniquacR = 0.857, UniquacQ = 0.94, ChaoSeadAF = 0.019, ChaoSeadSP = 8181.93, ChaoSeadLV = 0.0280225);
end Oxygen;

end database;