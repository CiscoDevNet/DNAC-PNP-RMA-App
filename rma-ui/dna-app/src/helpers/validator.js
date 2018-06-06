import RegEx from "./regex";

const validateRegex = (type, val) => {
	const {regex} = RegEx[type];
	const regExp = new RegExp(regex);
	return regExp.test(val) ? true: false;
};

export const isValidIP = (val) => {
	return validateRegex("ip", val);
};

export const isValidSerialNumber = (val) => {
	return validateRegex("serialNumber", val);
};

export default {
	isValidIP,
	isValidSerialNumber
};
