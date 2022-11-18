#include "GITHUB_PROJECT_NAME.h"

#include <vector>
#include <algorithm>
#include <maya/MItGeometry.h>
#include <maya/MFloatVectorArray.h>
#include <maya/MGlobal.h>
#include <maya/MFnMesh.h>

MTypeId GITHUB_PROJECT_NAME::id(0x001226FE);
MObject GITHUB_PROJECT_NAME::aPushLength;


void* GITHUB_PROJECT_NAME::creator() { return new GITHUB_PROJECT_NAME(); }
MStatus GITHUB_PROJECT_NAME::initialize() {
	MStatus status;
	MFnNumericAttribute nAttr;

	aPushLength = nAttr.create("pushLength", "pl", MFnNumericData::kFloat, 0.0f, &status);
	if (!status) return status;
	nAttr.setKeyable(true);
	status = addAttribute(aPushLength);
	if (!status) return status;
	status = attributeAffects(aPushLength, outputGeom);
	if (!status) return status;

	MGlobal::executeCommand("makePaintable -attrType \"multiFloat\" -sm \"deformer\" \"" DEFORMER_NAME "\" \"weights\";");

	return MStatus::kSuccess;
}

MStatus GITHUB_PROJECT_NAME::deform(
    MDataBlock& block, MItGeometry& iter,
    const MMatrix& m, unsigned int multiIndex
) {
    MStatus returnStatus;

    // Envelope data from the base class.
    MDataHandle envData = block.inputValue(envelope, &returnStatus);
    if (MS::kSuccess != returnStatus) return returnStatus;
    float env = envData.asFloat();

    // PushLength from the user
    MDataHandle hPushLen = block.inputValue(aPushLength, &returnStatus);
    if (MS::kSuccess != returnStatus) return returnStatus;
    float pushLen = hPushLen.asFloat();

    // iterate through each point in the geometry
    for (; !iter.isDone(); iter.next()) {
        MPoint pt = iter.position();
        MVector n = iter.normal();
        float weight = weightValue(block, multiIndex, iter.index());
        pt += (n * (weight * env * pushLen));
        iter.setPosition(pt);
    }
    return returnStatus;
}

