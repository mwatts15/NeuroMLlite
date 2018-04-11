from neuromllite import Network, Cell, InputSource, Population, Synapse
from neuromllite import Projection, RandomConnectivity, Input, Simulation
from neuromllite.NetworkGenerator import generate_and_run
from neuromllite.NetworkGenerator import generate_neuroml2_from_network
import sys

################################################################################
###   Build new network

net = Network(id='Example7_Brunel2000')
net.notes = 'Example 7: based on network of Brunel 2000'
net.parameters = { "N": 100 }

cell = Cell(id='ifcell', pynn_cell='IF_cond_alpha')
cell.parameters = { "tau_refrac":5, "i_offset":.1 }
net.cells.append(cell)


input_source = InputSource(id='iclamp0', 
                           pynn_input='DCSource', 
                           parameters={'amplitude':0.99, 'start':100., 'stop':900.})
                           
net.input_sources.append(input_source)


pE = Population(id='E', size='int(N*0.8)', component=cell.id)
pI = Population(id='I', size='int(N*0.2)', component=cell.id)

net.populations.append(pE)
net.populations.append(pI)

net.synapses.append(Synapse(id='ampa', 
                            pynn_receptor_type='excitatory', 
                            pynn_synapse_type='cond_alpha', 
                            parameters={'e_rev':-10, 'tau_syn':2}))
net.synapses.append(Synapse(id='gaba', 
                            pynn_receptor_type='inhibitory', 
                            pynn_synapse_type='cond_alpha', 
                            parameters={'e_rev':-80, 'tau_syn':10}))

net.projections.append(Projection(id='projEe',
                                  presynaptic=pE.id, 
                                  postsynaptic=pE.id,
                                  synapse='ampa',
                                  delay=2,
                                  weight=0.02,
                                  random_connectivity=RandomConnectivity(probability=.5)))
                                  
net.projections.append(Projection(id='projEI',
                                  presynaptic=pE.id, 
                                  postsynaptic=pI.id,
                                  synapse='ampa',
                                  delay=2,
                                  weight=0.02,
                                  random_connectivity=RandomConnectivity(probability=.5)))

net.projections.append(Projection(id='projIE',
                                  presynaptic=pI.id, 
                                  postsynaptic=pE.id,
                                  synapse='gaba',
                                  delay=2,
                                  weight=0.02,
                                  random_connectivity=RandomConnectivity(probability=.5)))

net.inputs.append(Input(id='stim',
                        input_source=input_source.id,
                        population=pE.id,
                        percentage=50))

print(net.to_json())
net.to_json_file('%s.json'%net.id)


################################################################################
###   Build Simulation object & save as JSON

sim = Simulation(id='SimExample7',
                 duration='1000',
                 dt='0.025',
                 recordTraces='all')
                 
sim.to_json_file()


################################################################################
###   Run in some simulators

print("**** Generating and running ****")


if '-pynnnest' in sys.argv:
    generate_and_run(sim, net, simulator='PyNN_NEST')
    
elif '-pynnnrn' in sys.argv:
    generate_and_run(sim, net, simulator='PyNN_NEURON')
    
elif '-pynnbrian' in sys.argv:
    generate_and_run(sim, net, simulator='PyNN_Brian')
    
elif '-jnml' in sys.argv:
    generate_and_run(sim, net, simulator='jNeuroML')
    
elif '-jnmlnrn' in sys.argv:
    generate_and_run(sim, net, simulator='jNeuroML_NEURON')
    
elif '-jnmlnetpyne' in sys.argv:
    generate_and_run(sim, net, simulator='jNeuroML_NetPyNE')
    
#else:
#    generate_and_run(sim, net, simulator='PyNN_NeuroML')

else:

    generate_neuroml2_from_network(net, 
                               nml_file_name='%s.net.nml'%net.id)

