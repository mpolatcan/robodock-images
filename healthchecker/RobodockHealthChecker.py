import subprocess, sys, json, time
from colorama import init, deinit, Fore, Back
from Config import Config


class ProdbaseHealthChecker:
    def __init__(self, config_filename):
        self.config = Config(config_filename=config_filename)

    def start_health_checker(self):
        print(Back.BLUE + Fore.LIGHTWHITE_EX + "###################### ZOOKEEPER HEALTHCHECK #######################" + Back.RESET + Fore.RESET)
        self.__health_check(service_name="zookeeper", checker=self.__zookeeper_health_check)

        print(Back.BLUE + Fore.LIGHTWHITE_EX + "######################### REDIS HEALTHCHECK ########################" + Back.RESET + Fore.RESET)
        self.__health_check(service_name="redis", checker=self.__redis_health_check)

        print(Back.BLUE + Fore.LIGHTWHITE_EX + "######################### KAFKA HEALTHCHECK ########################" + Back.RESET + Fore.RESET)
        self.__health_check(service_name="kafka", checker=self.__kafka_health_check)

        print(Back.BLUE + Fore.LIGHTWHITE_EX + "##################### ELASTICSEARCH HEALTHCHECK ####################" + Back.RESET + Fore.RESET)
        self.__health_check(service_name="elasticsearch", checker=self.__elasticsearch_health_check)

        print(Back.BLUE + Fore.LIGHTWHITE_EX + "##################### STORM WORKER HEALTHCHECK #####################" + Back.RESET + Fore.RESET)
        self.__health_check(service_name="storm-worker", checker=self.__storm_worker_health_check)

        print(Back.BLUE + Fore.LIGHTWHITE_EX + "##################### STORM NIMBUS HEALTHCHECK #####################" + Back.RESET + Fore.RESET)
        self.__health_check(service_name="storm-nimbus", checker=self.__storm_nimbus_health_check)

        print(Back.BLUE + Fore.LIGHTWHITE_EX + "####################### STORM UI HEALTHCHECK #######################" + Back.RESET + Fore.RESET)
        self.__health_check(service_name="storm-ui", checker=self.__storm_ui_health_check)

        print(Back.BLUE + Fore.LIGHTWHITE_EX + "###################### CASSANDRA HEALTH_CHECK ######################" + Back.RESET + Fore.RESET)
        self.__health_check(service_name="cassandra", checker=self.__cassandra_health_check)

    def __zookeeper_health_check(self, container_name):
        self.__print_message(message=container_name + ": ", status="ok" if self.__exec_cmd("echo ruok | nc " + container_name + " 2181") == "imok" else "fail")

    def __redis_health_check(self, container_name):
        node_address = self.__find_container_node(container_name)

        if self.__exec_cmd("docker -H tcp://" + str(node_address) + " ps | grep " + container_name) != "fail":
            self.__print_message(message=container_name + ": ", status=self.__exec_cmd("docker -H tcp://" + str(node_address) + " exec -it " + container_name + " redis-cli -c cluster info").splitlines()[0].split(":")[1])
        else:
            self.__print_message(message=container_name + ": ", status="fail")

    def __storm_nimbus_health_check(self, container_name):
        data = json.loads(self.__exec_cmd("curl http://storm-ui1:8080/api/v1/nimbus/summary"))

        for nimbus in data["nimbuses"]:
            if nimbus["host"].strip() == container_name:
                self.__print_message(message=container_name + ": ", status="ok" if nimbus["status"] != "Offline" else "fail")

    def __storm_worker_health_check(self, container_name):
        data = json.loads(self.__exec_cmd("curl http://storm-ui1:8080/api/v1/supervisor/summary"))

        workers = []
        for worker in data["supervisors"]:
            workers.append(worker["host"])

        self.__print_message(message=container_name + ": ", status="ok" if container_name in workers else "fail")

    def __storm_ui_health_check(self, container_name):
        self.__print_message(message=container_name + ": ", status="ok" if not self.__exec_cmd("curl http://" + container_name + ":8080/index.html").__eq__("fail") else "fail")

    def __elasticsearch_health_check(self, container_name):
        node_address = self.__find_container_node(container_name)
        container_ip_address = self.__exec_cmd("docker -H tcp://" + str(node_address) + " inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' " + container_name)

        nodes = []

        for node_info in self.__exec_cmd("curl http://elasticsearch1:9200/_cat/nodes").splitlines():
            nodes.append(node_info.split()[0])

        self.__print_message(message=container_name + ": ", status="ok" if nodes.__contains__(container_ip_address.strip()) else "fail")

    def __kafka_health_check(self, container_name):
        node_address = self.__find_container_node(container_name)

        status = "ok"

        self.__exec_cmd("docker -H tcp://" + str(node_address) + " exec -it " + container_name + " kafka-topics.sh --zookeeper zookeeper1 --create --topic test_topic --partitions 1 --replication-factor 1")

        list_res = self.__exec_cmd("docker -H tcp://" + str(node_address) + " exec -it " + container_name + " kafka-topics.sh --zookeeper zookeeper1 --list")

        if not list_res.splitlines().__contains__("test_topic"):
            status = "fail"

        self.__exec_cmd("docker -H tcp://" + str(node_address) + " exec -it " + container_name + " kafka-topics.sh --zookeeper zookeeper1 --delete --topic test_topic")

        list_res = self.__exec_cmd("docker -H tcp://" + str(node_address) + " exec -it " + container_name + " kafka-topics.sh --zookeeper zookeeper1 --list")

        if list_res.splitlines().__contains__("test_topic"):
            status = "fail"

        self.__print_message(message=container_name + ": ", status=status)

    def __cassandra_health_check(self, container_name):
        node_address = self.__find_container_node(container_name)
        container_ip_address = self.__exec_cmd("docker -H tcp://" + str(node_address) + " inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' " + container_name).strip()

        nodes = []

        index = 0
        for node_info in self.__exec_cmd("docker -H tcp://" + self.__find_container_node("cassandra1") + " exec -it cassandra1 nodetool status").splitlines():
            if index > 4 and node_info != '':
                nodes.append(node_info.split()[1])

            index += 1

        self.__print_message(message=container_name + ": ", status="ok" if container_ip_address in nodes else "fail")

    def __print_message(self, message, status):
        if status == "ok":
            print(Back.BLACK + Fore.LIGHTYELLOW_EX + time.strftime("%H:%M:%S") + " - [HEALTH-CHECKER]     | " + message + Fore.RESET + Back.RESET + Back.GREEN + Fore.LIGHTWHITE_EX + "HEALTHY" + Fore.RESET + Back.RESET)
        elif "fail":
            print(Back.BLACK + Fore.LIGHTYELLOW_EX + time.strftime("%H:%M:%S") + " - [HEALTH-CHECKER]     | " + message + Fore.RESET + Back.RESET + Back.RED + Fore.LIGHTWHITE_EX + "UNHEALTHY" + Fore.RESET + Back.RESET)
        else:
            pass

    def __exec_cmd(self, cmd):
        try:
            return subprocess.check_output([cmd], shell=True, stderr=subprocess.DEVNULL).decode("utf-8")
        except subprocess.CalledProcessError:
            return "fail"

    def __health_check(self, service_name, checker):
        containers = self.__get_containers(service_name=service_name)

        for i in containers:
            checker(i)

    def __get_containers(self, service_name):
        serv_containers = []

        for node in self.config.get(attr_name="robodock.healthchecker.nodes"):
            containers = self.__exec_cmd("docker -H tcp://" + str(node) + " ps -a | grep -w " + service_name + "[0-9+]")

            if not containers.__eq__("fail") and not containers.__eq__(""):
                for i in containers.splitlines():
                    tokens = i.split()
                    serv_containers.append(tokens[tokens.__len__() - 1])

        return serv_containers

    def __find_container_node(self, container_name):
        for node in self.config.get(attr_name="robodock.healthchecker.nodes"):
            try:
                res = self.__exec_cmd("docker -H tcp://" + node + " ps -a | grep " + container_name)

                if not res.__eq__("fail") and not res.__eq__(""):
                    return node
            except subprocess.CalledProcessError:
                continue


if __name__ == "__main__":
    init()
    ProdbaseHealthChecker(sys.argv[1]).start_health_checker()
    deinit()
