class Weather_tree():
    def __init__(self):
        import codecs
        file_data = codecs.open('weather.data', 'r')
        self.datas = []
        for line in file_data.read().split('\n'):
            outlook, temperature, humidity, windy, val = line.split(' ')
            self.datas.append({'option': {'outlook': outlook,
                                          'temperature': temperature,
                                          'humidity': humidity,
                                          'windy': windy}, 
                            'value': val})
        self.tree = Tree(self.datas)
        file_data.close()

    def get_tree(self):
        return self.tree
            
class Tree():
    def __init__(self, datas):
        self.datas = datas
            
    def info_measure(self, args):
        import math
        arg1 = int(args[0])
        arg2 = int(args[1])
        if arg1 == 0 or arg2 == 0:
            return 0
        s = arg1 + arg2
        measure = -(arg1/s) * math.log2(arg1/s) - (arg2/s) * math.log2(arg2/s)
        return measure
        
    def average_info_measure(self, args):
        s = 0
        for i in args:
            s += i[0] + i[1]
        info = 0
        for i in args:
            info += ((i[0]+i[1]) / s) * self.info_measure(i)
        return info
        
    def get_values_by_key(self, arg_key, arg_value):
        yes_count = 0
        no_count = 0
        for i in self.datas:
            if i['option'][arg_key] == arg_value:
                if i['value'] == 'yes':
                    yes_count += 1
                else:
                    no_count += 1
        return yes_count, no_count
    
    def get_all_values(self):
        yes_count = 0
        no_count = 0
        for i in self.datas:
            if i['value'] == 'yes':
                yes_count += 1
            else:
                no_count += 1
        return yes_count, no_count
    
    def get_key_values(self, arg_key):
        values = set()
        for i in self.datas:
            values.add(i['option'][arg_key])
        return values
    
    def gain_measure(self, option_key):
        counts = []
        for i in self.get_key_values(option_key):
            counts.append(self.get_values_by_key(option_key, i))
        info = self.info_measure(self.get_all_values()) - self.average_info_measure(counts)
        return info
    
    def build_tree(self):
        if self.get_all_values()[1] == 0:
            tree = {'leaf':'Yes'}
            return tree
        elif self.get_all_values()[0] == 0:
            tree = {'leaf':'No'}
            return tree
        best_option_key = None
        max_gain_measure = 0
        for i in self.datas[0]['option'].keys():
            curr_gain_measure = self.gain_measure(i)
            if max_gain_measure < curr_gain_measure:
                best_option_key = i
                max_gain_measure = curr_gain_measure
        tree = {'node':best_option_key,'branches':{}}
        for i in self.get_key_values(best_option_key):
            tree['branches'][i] = Tree(self.build_subtree(best_option_key, i))
        return tree
        
    def build_subtree(self, option_key, option_value):
        sub_datas = []
        for i in self.datas:
            if i['option'][option_key] == option_value:
                sub_datas.append(i)
        return sub_datas
        
    def print_tree(self):
        curr_t = self.build_tree()
        if curr_t.get('leaf'):
            print(curr_t['leaf'])
            return
        print(curr_t['node'],'::')
        for i in curr_t['branches'].keys():
            print('--', i)
            curr_t['branches'][i].print_tree()
        
    def test(self, options):
        curr_t = self.build_tree()
        if curr_t.get('leaf'):
            # print('returning ',curr_t['leaf'])
            return curr_t['leaf']
        return curr_t['branches'][options[curr_t['node']]].test(options)
        # while not curr_t.get('leaf'):
        #    if curr_t['branches'][options[curr_t['node']]]:
        #        curr_t = curr_t['branches'][options[curr_t['node']]]
        # return ['leaf']
        
a = Weather_tree()
t = a.get_tree()

import codecs
f = codecs.open('test.data', 'r')
for i in f.read().split('\n'):
    arr = i.split(' ')
    print(t.test({'outlook': arr[0], 'temperature': arr[1],
              'humidity': arr[2], 'windy': arr[3]}))