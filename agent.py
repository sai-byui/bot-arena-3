from copy import deepcopy

class Agent:
    def __init__(self, agent_name="", environment=None):
        self.agent_info = {}
        self.collected_info = {}
        self.agent_name = agent_name
        self.instance = None
        self.environment = environment
        Agent.__agent_list[agent_name] = self


    __agent_list = {}

    def ask(self, agent_name, variable_name):
        agent = Agent.__agent_list[agent_name]
        return deepcopy(getattr(agent, variable_name))

    def share(self, agent_name, variable_name):
        agent = Agent.__agent_list[agent_name]
        return getattr(agent, variable_name)

    def report(self, manager, data_name, data):
        manager.collected_info[self.agent_name + "." + data_name] = data




