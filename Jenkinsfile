stage("Clean") {
    node("sandy") {
        // Delete and initialise target
        if (fileExists("target")) {
            sh "rm -f target/*"
        } else {
            sh "mkdir target"
        }
    }
}
stage("Checkout") {
    node("sandy") {
        // Checkout tvheadend from GitHub and grab version details
    	dir ("scm") {
    		git url: "https://github.com/tvheadend/tvheadend", branch: params.build_tag
    		commit_tag = sh(script: 'git rev-list -n 1 HEAD', returnStdout: true).trim()
    		version_tag = sh(script: 'git describe', returnStdout: true).trim()
    	}
    	// Checkout build repository
    	dir ("scm_build") {
    	    git "https://github.com/matthera/tvheadend_test"
    	}
    	ver = version_info(version_tag)
    }
}
stage ("Build RPMS") {
    node ("sandy") {
        // Create spec file
        spec = "tvheadend-${ver['major_no']}.${ver['minor_no']}-${ver['build_no']}~g${ver['short_commit']}.spec"
        echo "Creating spec file: ${spec}"
        sh "sed '1s/\\[commit\\]/${commit_tag}/;2s/\\[short_commit\\]/${ver['short_commit']}/;3s/\\[major_no\\]/${ver['major_no']}/;4s/\\[minor_no\\]/${ver['minor_no']}/;5s/\\[build_no\\]/${ver['build_no']}/' scm_build/tvheadend.spec > target/${spec}"
        archiveArtifacts artifacts: "target/${spec}", fingerprint: true

        // Using fedora mock builder docker image
        docker.withRegistry('http://localhost:5000/') {
            mock = docker.image "matthera/fedora-rpmbuild:latest"
            mock.inside("--privileged --cap-add SYS_ADMIN", {
                // Create SRPM
            	dist = sh(script: 'rpm -E \'%dist\'', returnStdout: true).trim()
            	arch = sh(script: 'rpm -E \'%_arch\'', returnStdout: true).trim()
            	srpm = "tvheadend-${ver['major_no']}.${ver['minor_no']}-${ver['build_no']}~g${ver['short_commit']}${dist}.src.rpm"
            	echo "Creating SRPM: ${srpm}"
                sh "cp target/${spec} /home/build/rpmbuild/SPECS"
                sh "spectool -g -R /home/build/rpmbuild/SPECS/${spec}"
                sh "mock -r fedora-25-x86_64-rpmfusion_free --buildsrpm --spec /home/build/rpmbuild/SPECS/${spec} --sources /home/build/rpmbuild/SOURCES"
                sh "cp /var/lib/mock/fedora-25-x86_64/result/${srpm} /home/build/rpmbuild/SRPMS"
                sh "cp /var/lib/mock/fedora-25-x86_64/result/${srpm} target"
                archiveArtifacts artifacts: "target/${srpm}", fingerprint: true
                
                // Create RPMS
                rpm = "tvheadend-${ver['major_no']}.${ver['minor_no']}-${ver['build_no']}~g${ver['short_commit']}${dist}.${arch}.rpm"
                drpm = "tvheadend-debuginfo-${ver['major_no']}.${ver['minor_no']}-${ver['build_no']}~g${ver['short_commit']}${dist}.${arch}.rpm"
                echo "Creating RPM: ${rpm}"
                sh "mock -r fedora-25-x86_64-rpmfusion_free /home/build/rpmbuild/SRPMS/${srpm}"
                sh "cp /var/lib/mock/fedora-25-x86_64/result/${rpm} target"
                archiveArtifacts artifacts: "target/${rpm}", fingerprint: true
                sh "cp /var/lib/mock/fedora-25-x86_64/result/${drpm} target"
                archiveArtifacts artifacts: "target/${drpm}", fingerprint: true
            })
        }
    }
}
@NonCPS
def version_info(version_tag) {
    def matcher = version_tag =~ 'v([0-9]+)\\.([0-9]+).*-([0-9]+)-g(.+)'
    [major_no: matcher[0][1], minor_no: matcher[0][2], build_no: matcher[0][3], short_commit: matcher[0][4]]
}
