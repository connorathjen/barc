#!/usr/bin/env python

# ---------------------------------------------------------------------------
# Licensing Information: You are free to use or extend these projects for 
# education or reserach purposes provided that (1) you retain this notice
# and (2) you provide clear attribution to UC Berkeley, including a link 
# to http://barc-project.com
#
# Attibution Information: The barc project ROS code-base was developed
# at UC Berkeley in the Model Predictive Control (MPC) lab by Jon Gonzales
# (jon.gonzales@berkeley.edu). The cloud services integation with ROS was developed
# by Kiet Lam  (kiet.lam@berkeley.edu). The web-server app Dator was 
# based on an open source project by Bruce Wootton
# ---------------------------------------------------------------------------

from numpy import sin, cos, tan, arctan, array, dot
from numpy import sign, argmin, sqrt, abs, pi
import rospy

def bikeFE(x, y, psi, v, a, d_f, a0,m, Ff, theta, ts):
    """
    process model
    """
    # external parameters
    l_f                    = 1.5
    l_r                    = 1.5
    g                      = 9.8

    # compute slip angle
    beta = arctan(l_r/(l_r + l_f)*tan(d_f)) 
    F_d = a0*v*v
    F_ext = -(F_d + m*g*sin(theta) + Ff)

    # compute next state
    x_next      = x + (v*cos(psi + beta))*ts
    y_next      = y + (v*sin(psi + beta))*ts
    psi_next    = psi + (v/l_r*sin(beta))*ts
    v_next      = v + (a + F_ext/m)*ts

    return array([x_next, y_next, psi_next, v_next])