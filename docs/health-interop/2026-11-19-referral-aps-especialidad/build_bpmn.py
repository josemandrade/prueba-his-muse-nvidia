#!/usr/bin/env python3
"""Build BPMN 2.0 files for the referral case from data tables.

Usage: python3 build_bpmn.py <part>   (part = referral-triage |
       scheduling-counterreferral | status-query)
Writes 02-bpmn-model-<part>.bpmn next to this script's case folder.

The geometry is hand-laid-out on a grid (see the PARTS tables); every
flow's waypoints are explicit and orthogonal. Verify with
python3 check_bpmn.py --check <file> and render with
python3 render_bpmn.py <file> <file>.svg
"""
import sys
import xml.etree.ElementTree as ET

NS_BPMN = 'http://www.omg.org/spec/BPMN/20100524/MODEL'
NS_DI = 'http://www.omg.org/spec/BPMN/20100524/DI'
NS_DC = 'http://www.omg.org/spec/DD/20100524/DC'
NS_DDI = 'http://www.omg.org/spec/DD/20100524/DI'
NS_XSI = 'http://www.w3.org/2001/XMLSchema-instance'

ET.register_namespace('', NS_BPMN)
ET.register_namespace('di', NS_DI)
ET.register_namespace('dc', NS_DC)
ET.register_namespace('ddi', NS_DDI)
ET.register_namespace('xsi', NS_XSI)

# node: (tag, name, x, y, w, h, extra-dict)
# extra keys: attachedTo, cancelActivity ('true'/'false'), event ('timer' |
# 'message'), isExpanded ('false' for collapsed sub-process)
# flow: (kind, id, name, source, target, [(x, y), ...])
#   kind: 'sequence' | 'message'
# pool: (id, name, x, y, w, h, lanes=[(id, name, y, h, [node ids])])


def q(ns, tag):
    return '{%s}%s' % (ns, tag)


def build(part_id, pools, nodes, flows, out_path):
    root = ET.Element(q(NS_BPMN, 'definitions'), {
        'id': 'defs_' + part_id,
        'targetNamespace': 'http://example.org/referral/' + part_id,
        'exporter': 'build_bpmn.py', 'exporterVersion': '1.0'})
    collab = ET.SubElement(root, q(NS_BPMN, 'collaboration'),
                           {'id': 'collab_' + part_id})
    # one process per pool
    for pid, pname, px, py, pw, ph, lanes in pools:
        ET.SubElement(collab, q(NS_BPMN, 'participant'),
                      {'id': pid, 'name': pname,
                       'processRef': 'proc_' + pid})
    for kind, fid, fname, src, tgt, wps in flows:
        if kind == 'message':
            ET.SubElement(collab, q(NS_BPMN, 'messageFlow'),
                          {'id': fid, 'name': fname,
                           'sourceRef': src, 'targetRef': tgt})
    for pid, pname, px, py, pw, ph, lanes in pools:
        proc = ET.SubElement(root, q(NS_BPMN, 'process'),
                             {'id': 'proc_' + pid, 'isExecutable': 'false'})
        lane_set = ET.SubElement(proc, q(NS_BPMN, 'laneSet'),
                                 {'id': 'lanes_' + pid})
        for lid, lname, ly, lh, node_ids in lanes:
            lane = ET.SubElement(lane_set, q(NS_BPMN, 'lane'),
                                 {'id': lid, 'name': lname})
            for nid in node_ids:
                ET.SubElement(lane, q(NS_BPMN, 'flowNodeRef')).text = nid
        for nid, (tag, name, x, y, w, h, extra) in nodes.items():
            if nid not in [n for _, _, _, _, nids in lanes for n in nids]:
                continue
            # only nodes belonging to this pool's lanes
            el = ET.SubElement(proc, q(NS_BPMN, tag), {'id': nid})
            if name:
                el.set('name', name)
            if tag == 'boundaryEvent':
                el.set('attachedToRef', extra['attachedTo'])
                el.set('cancelActivity',
                       extra.get('cancelActivity', 'false'))
            if tag == 'subProcess':
                el.set('isExpanded', extra.get('isExpanded', 'false'))
            ev = extra.get('event')
            if ev == 'timer':
                ET.SubElement(el, q(NS_BPMN, 'timerEventDefinition'),
                              {'id': nid + '_timerdef'})
            elif ev == 'message':
                ET.SubElement(el, q(NS_BPMN, 'messageEventDefinition'),
                              {'id': nid + '_msgdef'})
        for kind, fid, fname, src, tgt, wps in flows:
            if kind != 'sequence':
                continue
            # sequence flows live in the process owning both endpoints
            src_pool = pool_of(src, pools)
            tgt_pool = pool_of(tgt, pools)
            if src_pool == pid and tgt_pool == pid:
                ET.SubElement(proc, q(NS_BPMN, 'sequenceFlow'),
                              {'id': fid, 'name': fname,
                               'sourceRef': src, 'targetRef': tgt})
    # DI
    diagram = ET.SubElement(root, q(NS_DI, 'BPMNDiagram'),
                            {'id': 'diag_' + part_id})
    plane = ET.SubElement(diagram, q(NS_DI, 'BPMNPlane'),
                          {'id': 'plane_' + part_id,
                           'bpmnElement': 'collab_' + part_id})
    shape_n = 0
    for pid, pname, px, py, pw, ph, lanes in pools:
        shape_n += 1
        s = ET.SubElement(plane, q(NS_DI, 'BPMNShape'),
                          {'id': 'di_%s' % pid, 'bpmnElement': pid})
        ET.SubElement(s, q(NS_DC, 'Bounds'),
                      {'x': str(px), 'y': str(py),
                       'width': str(pw), 'height': str(ph)})
        for lid, lname, ly, lh, node_ids in lanes:
            shape_n += 1
            s = ET.SubElement(plane, q(NS_DI, 'BPMNShape'),
                              {'id': 'di_%s' % lid, 'bpmnElement': lid})
            ET.SubElement(s, q(NS_DC, 'Bounds'),
                          {'x': str(px), 'y': str(ly),
                           'width': str(pw), 'height': str(lh)})
    for nid, (tag, name, x, y, w, h, extra) in nodes.items():
        shape_n += 1
        attrs = {'id': 'di_%s' % nid, 'bpmnElement': nid}
        if tag == 'subProcess':
            attrs['isExpanded'] = extra.get('isExpanded', 'false')
        s = ET.SubElement(plane, q(NS_DI, 'BPMNShape'), attrs)
        ET.SubElement(s, q(NS_DC, 'Bounds'),
                      {'x': str(x), 'y': str(y),
                       'width': str(w), 'height': str(h)})
    for kind, fid, fname, src, tgt, wps in flows:
        e = ET.SubElement(plane, q(NS_DI, 'BPMNEdge'),
                          {'id': 'di_%s' % fid, 'bpmnElement': fid})
        for (wx, wy) in wps:
            ET.SubElement(e, q(NS_DDI, 'waypoint'),
                          {'x': str(wx), 'y': str(wy)})
    tree = ET.ElementTree(root)
    ET.indent(tree, space='  ')
    tree.write(out_path, encoding='utf-8', xml_declaration=True)
    print('wrote %s (%d shapes, %d flows)'
          % (out_path, shape_n, len(flows)))


def pool_of(nid, pools):
    for pid, pname, px, py, pw, ph, pool_lanes in pools:
        for lid, lname, ly, lh, node_ids in pool_lanes:
            if nid in node_ids:
                return pid
    return None


if __name__ == '__main__':
    from parts_data import PARTS
    part = sys.argv[1]
    pools, nodes, flows = PARTS[part]
    build(part, pools, nodes, flows,
          '02-bpmn-model-%s.bpmn' % part)
