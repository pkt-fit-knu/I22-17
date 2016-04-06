class Iris():
    def __init__(self):
        import codecs
        file_data = codecs.open('iris.data', 'r')
        lines = file_data.read().split('\n')
        self.iris_args = []
        for i in range(0, len(lines)):
            self.iris_args.append(lines[i].split(','))
        self.N = len(self.iris_args)
        file_data.close()


    def sort(self, param):
        for i in range(0, self.N-1):
            min_ind = i
            for j in range(i+1, self.N):
                if self.iris_args[j][param] < self.iris_args[min_ind][param]:
                    min_ind = j
            self.iris_args[min_ind], self.iris_args[i] = self.iris_args[i], self.iris_args[min_ind] 

    def take_rule(self, param, limit=3):
        self.sort(param)
        count_class = {'Iris-setosa' : 0, 'Iris-versicolor':0, 'Iris-virginica':0}
        left = 0
        parts = []
        i = 0
        while i < self.N:
            category = self.iris_args[i][4]
            count_class[category] += 1
            if count_class[category] >= limit or i == self.N-1:
                count_class = {'Iris-setosa' : 0, 'Iris-versicolor':0, 'Iris-virginica':0}
                while i+1<self.N and self.iris_args[i+1][4] == category:
                    i += 1
                if len(parts) > 0 and parts[len(parts)-1][2] == category:
                    parts[len(parts)-1] = (parts[len(parts)-1][0],
                        float(self.iris_args[i][param]), category)
                else:
                    parts.append((float(self.iris_args[left][param]),
                        float(self.iris_args[i][param]),
                        category))
                left = i + 1
            i += 1
        # print('param=',param,'parts=',parts)
        
        def get_class_on_rule(value):
            for part in parts:
                if value >= part[0] and value <= part[1]:
                    return part[2]                       
            return 'I don`t know'
        return get_class_on_rule
                             
            

    def take_names(self, param):
        names = []
        rule = self.take_rule(param)
        for i in range(0, self.N):
            value = float(self.iris_args[i][param])
            names.append(rule(value))
        return names

    def find_best_rule(self):
        min_errors = None
        best_param = None
        for param in range(0, 4):
            curr_errors = 0
            param_names = self.take_names(param)
            for i in range(0, len(param_names)):
                if param_names[i] != self.iris_args[i][4]:
                    curr_errors += 1
            if min_errors is None or curr_errors < min_errors:
                min_errors = curr_errors
                best_param = param
        print('Best Column =', best_param)
        return best_param

    def print_result(self):
        import codecs
        # file_res = codecs.open('iris_result.txt', 'w')
        column = self.find_best_rule()
        res_names = self.take_names(column)
        plus_count = 0
        all_count = 0
        for i in range(0,len(self.iris_args)):
            sign = '+' if res_names[i] == self.iris_args[i][4] else '-'
            if sign == '+':
                plus_count += 1
            all_count += 1
            # file_res.write('%s%s\n' % (sign, res_names[i]))
            print('%s%s' % (sign, res_names[i]))
        print(str(100 * (plus_count / all_count)) + '%')
        # file_res.write(str(100 * (plus_count / all_count))+'%')
        # file_res.close()


a = Iris()
a.print_result()
