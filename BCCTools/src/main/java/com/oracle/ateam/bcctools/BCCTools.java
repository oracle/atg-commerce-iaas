/**
 * Copyright (c) 2017, Oracle Corporation
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification, are permitted provided
 * that the following conditions are met:
 *
 *     * Redistributions of source code must retain the above copyright notice, this list of
 *       conditions and the following disclaimer.
 *
 *     * Redistributions in binary form must reproduce the above copyright notice, this list
 *       of conditions and the following disclaimer in the documentation and/or other materials
 *       provided with the distribution.
 *
 *     * Neither the name of Oracle nor the names of its contributors may be used to endorse or
 *       promote products derived from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
 * PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL ORACLE BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
 * GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

package com.oracle.ateam.bcctools;

import java.io.ByteArrayInputStream;
import java.io.InputStream;
import java.util.Iterator;
import java.util.List;

import javax.xml.bind.DatatypeConverter;

import atg.deployment.common.DeploymentException;
import atg.deployment.server.DeploymentServer;
import atg.deployment.server.Target;
import atg.deployment.server.topology.TargetDef;
import atg.deployment.server.topology.TopologyDef;
import atg.deployment.server.topology.TopologyManager;
import atg.nucleus.GenericService;

/**
 * Helper methods for accessing CA through REST calls.
 * 
 * @author mshanley
 *
 */
public class BCCTools extends GenericService {

	/**
	 * Attempt to find the target ID based on the target name
	 * 
	 * @param targetName
	 *            The name of the target to try to find an ID for
	 * @return TargetDef if found. Else null.
	 * @throws DeploymentException
	 */
	public TargetDef getTargetByName(String targetName) throws DeploymentException {

		if (isLoggingDebug())
			logDebug("checking for name " + targetName);
		TopologyManager manager = getDeploymentServer().getTopologyManager();
		TopologyDef surrogate = manager.getSurrogateTopology();
		List surrogateTargets = surrogate.getTargets();

		// check surrogate topology first
		for (Iterator tItr = surrogateTargets.iterator(); tItr.hasNext();) {
			TargetDef surrogateTarget = (TargetDef) tItr.next();
			if (surrogateTarget.getDisplayName().equals(targetName)) {
				if (isLoggingDebug())
					logDebug("found surrogate target " + targetName);
				return surrogateTarget;
			}
		}

		return null;
	}

	/**
	 * Attempt to find the target ID based on the target name
	 * 
	 * @param targetName
	 *            The name of the target to try to find an ID for
	 * @return Target if found. Else null.
	 * @throws DeploymentException
	 */
	public Target getLiveTargetByName(String targetName) throws DeploymentException {

		if (isLoggingDebug())
			logDebug("checking for name " + targetName);
		TopologyManager manager = getDeploymentServer().getTopologyManager();
		TopologyDef surrogate = manager.getSurrogateTopology();
		Target[] liveTargets = getDeploymentServer().getTargets();

		if (liveTargets != null) {
			for (Target t : liveTargets) {
				if (isLoggingDebug())
					logDebug("found live target " + targetName);
				if (t.getName().equals(targetName)) {
					return t;
				}
			}
		}

		return null;
	}

	/**
	 * Import an already defined XML topology for CA. Incoming data must be base
	 * 64 encoded.
	 * 
	 * @param xmlData
	 *            base64 encoded topology XML
	 * @return true if no errors
	 */
	public boolean importTopologyFromXML(String xmlData) {

		if (isLoggingDebug())
			logDebug("data passed in is " + xmlData);

		byte[] fileAsBytes = DatatypeConverter.parseBase64Binary(xmlData);

		InputStream stream = new ByteArrayInputStream(fileAsBytes);
		DeploymentServer server = getDeploymentServer();
		try {
			server.importTopologyFromXML(stream);
		} catch (DeploymentException de) {
			if (isLoggingError())
				logError(de);
			return false;
		}

		return true;
	}

	// ---------- Property: deploymentServer ----------
	DeploymentServer mDeploymentServer;

	/**
	 * @return Returns the deploymentServer.
	 */
	public DeploymentServer getDeploymentServer() {
		return mDeploymentServer;
	}

	/**
	 * @param pDeploymentServer
	 *            The deploymentServer to set.
	 */
	public void setDeploymentServer(DeploymentServer pDeploymentServer) {
		mDeploymentServer = pDeploymentServer;
	}
}
