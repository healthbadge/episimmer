import Simulate
import ReadFile
import os.path as osp
import Utility
import Time
import math
import matplotlib.pyplot as plt
import numpy as np
import pickle

def print_no_infections(avg_dict, time_steps):

    fp = open('IITJ_Stochastic_SIR/tests_dict.pickle', 'rb')
    tests_dict = pickle.load(fp)
    for time_step in range(time_steps):
        if time_step in tests_dict.keys():
            print(avg_dict['Infected'][time_step])

def avg_pos(dict, time_steps):
    avg_list = []
    for time_step in range(time_steps):
        if(dict[0][time_step]['Total Agents Tested']!=0):
            sum = 0.0
            for k in dict.keys():
                # print(time_step, dict[k][time_step]['Total Positive Results'])
                sum += dict[k][time_step]['Total Positive Results']
            sum /= len(dict.keys())
            avg_list.append(sum)
    return avg_list

def get_bounds_dict(dict, time_steps, len_ls):
    maxls = [0]*(len_ls)
    minls = [math.inf]*(len_ls)
    ctr = 0
    for time_step in range(time_steps):
        if(dict[0][time_step]['Total Agents Tested']!=0):
            for k in dict.keys():
                maxls[ctr] = max(maxls[ctr], dict[k][time_step]['Total Positive Results'])
                minls[ctr] = min(minls[ctr], dict[k][time_step]['Total Positive Results'])
            ctr+=1
    return maxls, minls


def plotPosResults(avg_list, maxls, minls, plot=True):
    """
    ### IITJ
    target_ls = [2,2,3,10,12,15,9,8,3,8,5,27,1,4,13,6,25,6,2,4,1,6,3,2,0,1,2]
    date_ls = ["3/10/2021","3/18/2021","3/22/2021","3/28/2021","3/30/2021","3/31/2021","4/1/2021","4/6/2021","4/7/2021"\
                ,"4/10/2021","4/14/2021","4/19/2021","4/21/2021","4/22/2021","4/28/2021","5/5/2021","5/7/2021","5/10/2021"\
                ,"5/12/2021","5/14/2021","5/17/2021","5/19/2021","5/21/2021","5/24/2021","5/26/2021","5/28/2021","5/31/2021"]
    """
    """
    ### IIITH_5_months
    target_ls = [0,0,0,0,0,0,0,0,0,4,3,3,20,6,10,0,0,0,0,0,1]
    date_ls = ["03.02.2021","08.02.2021","15.02.2021","22.02.2021","01.03.2021","08.03.2021","15.03.2021","22.03.2021",\
                "28.03.2021","05.04.2021","11.04.2021","12.04.2021","19.04.2021","26.04.2021","06.05.2021","11.05.2021",\
                "16.05.2021","23.05.2021","30.05.2021","07.06.2021","14.06.2021"]
    """
    ### IIITH_3_months
    #target_ls = [0,4,2,4,20,6,10,0,0,0,0,0,1]
    #date_ls = ["28.03.2021","05.04.2021","11.04.2021","12.04.2021","19.04.2021","26.04.2021","06.05.2021","11.05.2021",\
    #            "16.05.2021","23.05.2021","30.05.2021","07.06.2021","14.06.2021"]
    x=np.arange(0,len(avg_list))
    plt.plot(avg_list, label="Predicted")
    plt.plot(target_ls, label="Target")
    plt.fill_between(x, minls, maxls, alpha=0.2, linewidth=0)
    plt.title('Predicted Student Positives')
    plt.legend(loc='upper right')
    plt.ylabel('Number of students tested positive')
    plt.xlabel('Dates')
    plt.xticks(x,date_ls,rotation="vertical")
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999',linestyle='-', alpha=0.2)
    fig = plt.gcf()
    if plot:
        plt.show()
    return fig


class World():
    def __init__(self, config_obj, model, policy_list, event_restriction_fn, agents_filename, interactionFiles_list, probabilistic_interactionFiles_list, locations_filename, eventFiles_list, one_time_event_file):
        self.config_obj = config_obj
        self.policy_list = policy_list
        self.event_restriction_fn = event_restriction_fn
        self.agents_filename = agents_filename
        self.locations_filename = locations_filename
        self.model = model
        self.interactionFiles_list = interactionFiles_list
        self.probabilistic_interactionsFiles_list=probabilistic_interactionFiles_list
        self.eventFiles_list = eventFiles_list
        self.one_time_event_file = one_time_event_file
        self.positives ={}

    def one_world(self):

        time_steps = self.config_obj.time_steps

        Time.Time.new_world()

        # Initialize agents
        agents_obj = ReadFile.ReadAgents(self.agents_filename, self.config_obj)

        # Intialize locations
        locations_obj = ReadFile.ReadLocations(self.locations_filename, self.config_obj)

        # Initialize one time events
        oneTimeEvent_obj = ReadFile.ReadOneTimeEvents(self.one_time_event_file)

        sim_obj = Simulate.Simulate(self.config_obj, self.model, self.policy_list, self.event_restriction_fn, agents_obj, locations_obj)
        sim_obj.onStartSimulation()

        for current_time_step in range(time_steps):
            sim_obj.onStartTimeStep(self.interactionFiles_list, self.eventFiles_list, self.probabilistic_interactionsFiles_list, oneTimeEvent_obj)
            sim_obj.handleTimeStepForAllAgents()
            sim_obj.endTimeStep()
            Time.Time.increment_current_time_step()

        end_state = sim_obj.endSimulation()


        return end_state, agents_obj, locations_obj

    # Averages multiple simulations and plots a single plot
    def simulate_worlds(self):

        args = Utility.parse_args()
        plot = args.noplot
        anim = args.animate

        tdict = {}
        t2_dict = {}
        maxdict={}
        mindict={}
        for state in self.model.individual_state_types:
            tdict[state] = [0]*(self.config_obj.time_steps+1)
            t2_dict[state] = [0]*(self.config_obj.time_steps+1)
            maxdict[state] = [0]*(self.config_obj.time_steps+1)
            mindict[state] = [math.inf]*(self.config_obj.time_steps+1)

        for i in range(self.config_obj.worlds):
            print("Running World : ",i+1)
            sdict, _, _ = self.one_world()
            self.positives[i] = self.policy_list[0].statistics
            for state in self.model.individual_state_types:
                for j in range(len(tdict[state])):
                    tdict[state][j] += sdict[state][j]
                    t2_dict[state][j] += sdict[state][j]**2
                    maxdict[state][j] =max(maxdict[state][j],sdict[state][j])
                    mindict[state][j] =min(mindict[state][j],sdict[state][j])

        # Average number time series
        avg_dict = Utility.average(tdict, self.config_obj.worlds)
        print(avg_dict['Susceptible'][-1])

        #avg_positives = avg_pos(self.positives, self.config_obj.time_steps)
        #for el in avg_positives:
        #    print(el)
        # print_no_infections(avg_dict, self.config_obj.time_steps)
        #maxls, minls = get_bounds_dict(self.positives, self.config_obj.time_steps, len(avg_positives))
        #plotPosResults(avg_positives, maxls, minls)

        stddev_dict = Utility.stddev(tdict, t2_dict, self.config_obj.worlds)
        plottor = Utility.plotResults(self.model, avg_dict,stddev_dict, maxdict, mindict, plot)
        plottor.savefig(osp.join(self.config_obj.example_path,'results','results.jpg'))
        if anim:
            animator = Utility.animateResults(self.model.name, avg_dict)
            animator.save(osp.join(self.config_obj.example_path,'results','results.gif'))

        return avg_dict
