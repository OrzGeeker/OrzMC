class Spigot:

    build_tool_jar = 'https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar'
    
    def __init__(self, version):
        self.server_version = version

